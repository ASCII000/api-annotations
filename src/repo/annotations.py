from dataclasses import dataclass


@dataclass
class Annotation:
    title: str
    description: str
    url: str

class AnnotationsRepository:

    def get_annotations(self) -> list[Annotation]:
        fake_annotations = [
            Annotation(title="title1", description="description1", url="url1"),
            Annotation(title="title2", description="description2", url="url2"),
            Annotation(title="title3", description="description3", url="url3"),
        ]

        return fake_annotations
    
    def add_annotation(self, annotation: Annotation):
        pass
