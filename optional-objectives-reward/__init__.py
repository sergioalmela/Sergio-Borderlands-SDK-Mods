"""
Optional Objectives Reward Mod for SDK v3
Automatically rewards ALL optional objectives in Borderlands 2 and The Pre-Sequel
Rewards scale with playthrough difficulty (Normal/TVHM/UVHM)
"""

from typing import Any

import unrealsdk
from mods_base import Game, SliderOption, build_mod, hook, get_pc
from unrealsdk import logging
from unrealsdk.hooks import Type
from unrealsdk.unreal import UObject, WrappedStruct, BoundFunction

__version__: str = "1.0.0"
__version_info__: tuple[int, ...] = (1, 0, 0)


def on_slider_change(option: SliderOption, new_value: int) -> None:
    """Called when any slider value changes - reapply rewards."""
    logging.info(f"[Optional Objectives] Slider '{option.identifier}' changed to {new_value}, reapplying rewards...")
    apply_rewards()


# Configuration options
normal_slider = SliderOption(
    identifier="Normal Mode Reward",
    value=50,
    min_value=0,
    max_value=500,
    step=10,
    is_hidden=False,
    description="Reward percentage for Normal mode (50 = 50% of base reward)",
    on_change=on_slider_change,
)

tvhm_slider = SliderOption(
    identifier="TVHM Reward",
    value=100,
    min_value=0,
    max_value=500,
    step=10,
    is_hidden=False,
    description="Reward percentage for TVHM (100 = 100% of base reward)",
    on_change=on_slider_change,
)

uvhm_slider = SliderOption(
    identifier="UVHM Reward",
    value=200,
    min_value=0,
    max_value=500,
    step=10,
    is_hidden=False,
    description="Reward percentage for UVHM (200 = 200% of base reward)",
    on_change=on_slider_change,
)


def get_playthrough() -> int:
    """
    Get current playthrough number.

    Returns:
        0 for Normal, 1 for TVHM, 2 for UVHM
    """
    try:
        pc = get_pc()
        if pc is not None:
            return pc.GetCurrentPlaythrough()
    except Exception:
        pass
    return 0


def apply_rewards() -> None:
    """Apply rewards to all optional objectives in the game."""
    playthrough = get_playthrough()

    # For cash rewards, use decimal scaling (0.5, 1.0, 2.0)
    cash_scales = [
        normal_slider.value / 100.0,
        tvhm_slider.value / 100.0,
        uvhm_slider.value / 100.0,
    ]
    cash_scale = cash_scales[min(playthrough, 2)]

    # For XP rewards, use percentage values (50, 100, 200)
    xp_scales = [
        normal_slider.value,
        tvhm_slider.value,
        uvhm_slider.value,
    ]
    xp_scale = xp_scales[min(playthrough, 2)]

    playthrough_names = ["Normal", "TVHM", "UVHM"]
    logging.info(
        f"[Optional Objectives] Detected playthrough: {playthrough} ({playthrough_names[min(playthrough, 2)]})"
    )
    logging.info(
        f"[Optional Objectives] Applying rewards - Cash scale: {cash_scale}, XP scale: {xp_scale}"
    )

    all_missions = list(unrealsdk.find_all("MissionDefinition"))
    logging.info(f"[Optional Objectives] Found {len(all_missions)} total MissionDefinitions")

    count = 0
    for mission in all_missions:
        if not mission:
            continue

        try:
            # Access ObjectiveDefs, not Objectives
            if hasattr(mission, "ObjectiveDefs") and mission.ObjectiveDefs:
                for objective in mission.ObjectiveDefs:
                    if not objective:
                        continue

                    # Check if this is an optional objective using bObjectiveIsOptional
                    if hasattr(objective, "bObjectiveIsOptional") and objective.bObjectiveIsOptional:
                        # Set the credit reward
                        if hasattr(objective, "OptionalCreditRewardMultiplier"):
                            objective.OptionalCreditRewardMultiplier.BaseValueAttribute = None
                            objective.OptionalCreditRewardMultiplier.BaseValueConstant = 0.0
                            objective.OptionalCreditRewardMultiplier.BaseValueScaleConstant = cash_scale

                        # Set XP reward with proper scaling (percentage of base mission XP)
                        if hasattr(objective, "OptionalExperienceRewardPercentage"):
                            objective.OptionalExperienceRewardPercentage.BaseValueAttribute = None
                            objective.OptionalExperienceRewardPercentage.BaseValueConstant = xp_scale / 2000.0
                            objective.OptionalExperienceRewardPercentage.BaseValueScaleConstant = 1.0

                        count += 1
        except Exception as e:
            logging.error(f"[Optional Objectives] Error processing mission: {e}")
            continue

    logging.info(f"[Optional Objectives] Applied rewards to {count} optional objectives")


def on_enable() -> None:
    """Called when the mod is enabled."""
    logging.info("[Optional Objectives] Mod enabled")
    apply_rewards()


@hook("WillowGame.WillowPlayerController:WillowClientDisableLoadingMovie")
def on_map_loaded(
    obj: UObject,
    args: WrappedStruct,
    ret: Any,
    func: BoundFunction,
) -> None:
    """Hook that triggers when a map finishes loading - reapply rewards."""
    logging.info("[Optional Objectives] Map loaded, reapplying rewards...")
    apply_rewards()


mod = build_mod()