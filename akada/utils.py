from admin_app.models import Quest
from akada.models import GeneratedStudyMaterials


class NewStudyMaterialInstance:
    def __init__(self, topic: str, quest: Quest):
        self.topic = topic
        self.quest = quest


def _save_study_materials_instance(instances: list[NewStudyMaterialInstance]) -> bool:
    for instance in instances:
        if not GeneratedStudyMaterials.objects.filter(topic__contains=instance.topic, quest=instance.quest).exists():
            if len(instance.topic) > 0:
                study_material = GeneratedStudyMaterials()
                study_material.topic = instance.topic
                study_material.quest = instance.quest
                study_material.save()
    return True
