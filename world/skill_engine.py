"""
Skill engine — general proficiency system (0-100 per skill).

Provides get_skill_value and record_skill_use for appraisal checks
and passive skill advancement. Full implementation deferred to the
dedicated skill system plan.
"""


def get_skill_value(character, skill_name):
    """
    Return 0-100 skill value for a character.

    Reads from character.db.skills dict. Returns 0 if no skills set.
    """
    skills = character.db.skills or {}
    return skills.get(skill_name, 0)


def record_skill_use(character, skill_name):
    """
    Record a skill use for passive advancement tracking.

    Increments use counter on character.db.skill_uses. Full XP-based
    advancement logic will be implemented in the skill system plan.
    """
    skill_uses = character.db.skill_uses or {}
    skill_uses[skill_name] = skill_uses.get(skill_name, 0) + 1
    character.db.skill_uses = skill_uses
