"""
Main training entrypoint for MediaForge Vision.
"""

from __future__ import annotations

from pathlib import Path

import torch

from torch.utils.data import DataLoader
from torchvision import transforms

from ml.models.model import MediaForgeVision

from ml.training.vision_dataset import VisionDataset
from ml.training.loss import build_loss
from ml.training.optimizer import build_optimizer
from ml.training.scheduler import build_scheduler
from ml.training.trainer import Trainer
from ml.training.validator import Validator
from ml.training.metrics import Metrics
from ml.training.checkpoint import CheckpointManager
from ml.training.logging import ExperimentLogger

from ml.utils.config import load_config
from ml.utils.seed import seed_everything


# ==========================================================
# Device
# ==========================================================

def get_device() -> torch.device:

    if torch.cuda.is_available():
        return torch.device("cuda")

    return torch.device("cpu")


# ==========================================================
# Transforms
# ==========================================================

def build_transforms():

    train_transform = transforms.Compose(
        [
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
        ]
    )

    val_transform = transforms.Compose(
        [
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
        ]
    )

    return train_transform, val_transform


# ==========================================================
# Dataset
# ==========================================================

def build_datasets(config):

    train_transform, val_transform = build_transforms()

    train_dataset = VisionDataset(
        manifest=config["data"]["train_manifest"],
        transform=train_transform,
    )

    val_dataset = VisionDataset(
        manifest=config["data"]["val_manifest"],
        transform=val_transform,
    )

    return train_dataset, val_dataset


# ==========================================================
# Dataloader
# ==========================================================

def build_dataloaders(config):

    train_dataset, val_dataset = build_datasets(config)

    train_loader = DataLoader(
        train_dataset,
        batch_size=config["training"]["batch_size"],
        shuffle=True,
        num_workers=config["training"]["num_workers"],
        pin_memory=config["training"]["pin_memory"],
    )

    val_loader = DataLoader(
        val_dataset,
        batch_size=config["training"]["batch_size"],
        shuffle=False,
        num_workers=config["training"]["num_workers"],
        pin_memory=config["training"]["pin_memory"],
    )

    return train_loader, val_loader


# ==========================================================
# Train
# ==========================================================

def train():

    config = load_config(
        "ml/configs/training.yaml"
    )

    seed_everything(
        config["seed"]["value"]
    )

    device = get_device()

    experiment_name = config["experiment"]["name"]

    logger = ExperimentLogger(
        experiment_name=experiment_name,
        output_root=config["experiment"]["output_dir"],
    )

    logger.save_config(config)

    logger.info("=" * 70)
    logger.info("MediaForge Vision")
    logger.info("=" * 70)
    logger.info(f"Experiment : {experiment_name}")
    logger.info(f"Device      : {device}")

    train_loader, val_loader = build_dataloaders(
        config
    )

    logger.info(
        f"Training Images   : {len(train_loader.dataset)}"
    )

    logger.info(
        f"Validation Images : {len(val_loader.dataset)}"
    )

    model = MediaForgeVision(
        backbone="convnext_tiny",
        pretrained=True,
    )

    criterion = build_loss(config)

    optimizer = build_optimizer(
        model,
        config,
    )

    scheduler = build_scheduler(
        optimizer,
        config,
    )

    metrics = Metrics()

    trainer = Trainer(
        model=model,
        optimizer=optimizer,
        criterion=criterion,
        train_loader=train_loader,
        device=device,
    )

    validator = Validator(
        model=model,
        criterion=criterion,
        dataloader=val_loader,
        metrics=metrics,
        device=device,
    )

    checkpoint_manager = CheckpointManager(
        logger.directory
    )

    start_epoch = 0

    best_f1 = 0.0

    latest = checkpoint_manager.latest()

    if latest is not None:

        logger.info(
            f"Resuming from {latest.name}"
        )

        checkpoint = checkpoint_manager.load(
            model=model,
            optimizer=optimizer,
            scheduler=scheduler,
            filename=latest.name,
            map_location=device,
        )

        start_epoch = checkpoint["epoch"]+1

        best_f1 = checkpoint["best_metric"]

    epochs = config["training"]["epochs"]

    logger.info(
        f"Epochs      : {epochs}"
    )

    logger.info("=" * 70)

    # ======================================================
    # Training Loop
    # ======================================================

    for epoch in range(

        start_epoch,

        epochs,

    ):

        logger.info("")

        logger.info(
            "=" * 70
        )

        logger.info(
            f"Epoch {epoch + 1}/{epochs}"
        )

        logger.info(
            "=" * 70
        )

        # ------------------------------------------
        # Train
        # ------------------------------------------

        train_results = trainer.train_epoch()

        # ------------------------------------------
        # Validation
        # ------------------------------------------

        val_results = validator.validate()

        scheduler.step()

        current_lr = optimizer.param_groups[0]["lr"]

        logger.info(

            f"Train Loss : {train_results['loss']:.4f}"

        )

        logger.info(

            f"Val Loss   : {val_results['loss']:.4f}"

        )

        logger.info(

            f"Accuracy   : {val_results['accuracy']:.4f}"

        )

        logger.info(

            f"Precision  : {val_results['precision']:.4f}"

        )

        logger.info(

            f"Recall     : {val_results['recall']:.4f}"

        )

        logger.info(

            f"F1 Score   : {val_results['f1']:.4f}"

        )

        logger.info(

            f"Learning Rate : {current_lr:.8f}"

        )

        # ------------------------------------------
        # Log metrics
        # ------------------------------------------
        logger.log_metrics(

            epoch + 1,

            {

                "train_loss": train_results["loss"],

                "val_loss": val_results["loss"],

                "accuracy": val_results["accuracy"],

                "precision": val_results["precision"],

                "recall": val_results["recall"],

                "f1": val_results["f1"],

                "learning_rate": current_lr,

            },

        )

        # ------------------------------------------
        # Save latest checkpoint
        # ------------------------------------------

        checkpoint_manager.save(

            model=model,

            optimizer=optimizer,

            scheduler=scheduler,

            epoch=epoch + 1,

            best_metric=best_f1,

            config=config,

        )

        # ------------------------------------------
        # Save best model
        # ------------------------------------------

        if val_results["f1"] > best_f1:

            best_f1 = val_results["f1"]

            checkpoint_manager.save_best(

                model=model,

                optimizer=optimizer,

                scheduler=scheduler,

                epoch=epoch + 1,

                best_metric=best_f1,

                config=config,

            )

            logger.info(

                f"✓ New best model saved (F1 = {best_f1:.4f})"

            )

    logger.info("=" * 70)

    logger.info("Training Finished")

    logger.info(f"Best Validation F1 : {best_f1:.4f}")

    logger.info("=" * 70)


# ==========================================================
# Main
# ==========================================================

def main():

    train()


if __name__ == "__main__":

    main()