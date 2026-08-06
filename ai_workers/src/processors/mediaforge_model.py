import timm
import torch.nn as nn


class MediaForgeVision(nn.Module):

    def __init__(self):

        super().__init__()

        self.backbone = timm.create_model(
            "convnextv2_base.fcmae_ft_in22k_in1k",
            pretrained=False,
            num_classes=0,
            global_pool="avg",
        )

        in_features = self.backbone.num_features

        self.classifier = nn.Sequential(

            nn.LayerNorm(in_features),

            nn.Dropout(0.30),

            nn.Linear(in_features, 512),

            nn.GELU(),

            nn.Dropout(0.20),

            nn.Linear(512, 2),

        )

    def forward(self, x):

        features = self.backbone(x)

        return self.classifier(features)