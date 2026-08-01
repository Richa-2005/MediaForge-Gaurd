"""
MediaForge Vision Taxonomy

Canonical ontology for the MediaForge Vision Engine.

Every dataset adapter MUST map its native labels into this taxonomy.
No other module is allowed to define custom labels.
"""

from enum import Enum


# ============================================================
# PRIMARY TASK
# ============================================================

class Authenticity(str, Enum):
    """
    Primary forensic decision.

    This is the highest priority prediction.
    """

    AUTHENTIC = "authentic"
    NOT_AUTHENTIC = "not_authentic"
    SUSPICIOUS = "suspicious"
    INCONCLUSIVE = "inconclusive"


# ============================================================
# SECONDARY TASK
# ============================================================

class Origin(str, Enum):
    """
    Broad origin of the image.
    """

    CAMERA = "camera"
    AI_GENERATED = "ai_generated"
    EDITED = "edited"
    UNKNOWN = "unknown"


# ============================================================
# TERTIARY TASK
# ============================================================

class Technique(str, Enum):
    """
    Fine-grained manipulation / generation method.
    """

    NONE = "none"

    # ---------- AI Generation ----------
    AI_GENERATED = "ai_generated"
    # ---------- Image Editing ----------
    SPLICING = "splicing"
    COPY_MOVE = "copy_move"
    INPAINTING = "inpainting"
    REMOVAL = "removal"

    # ---------- Face Manipulation ----------
    FACE_SWAP = "face_swap"
    FACE_REENACTMENT = "face_reenactment"

    # ---------- Enhancement ----------
    AI_ENHANCEMENT = "ai_enhancement"

    # ---------- Other ----------
    SCREENSHOT = "screenshot"

    UNKNOWN = "unknown"


# ============================================================
# AI Generator Family
# ============================================================

class Generator(str, Enum):
    """
    Generator family.

    Used for metadata, future training and analysis.
    """

    NONE = "none"
    UNKNOWN = "unknown"

    ADM = "adm"
    BIGGAN = "biggan"
    GLIDE = "glide"
    MIDJOURNEY = "midjourney"
    STABLE_DIFFUSION_V5 = "stable_diffusion_v5"
    VQDM = "vqdm"
    WUKONG = "wukong"


# ============================================================
# Dataset Split
# ============================================================

class Split(str, Enum):

    TRAIN = "train"
    VAL = "val"
    TEST = "test"


# ============================================================
# Confidence
# ============================================================

class ConfidenceLevel(str, Enum):

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"