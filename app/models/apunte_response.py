from pydantic import BaseModel


class Answer:
    def __init__(self, sujeto, kilos=None, gramos=None, centimetros=None,
                 mililitros=None, grados=None, decimas=None):
        content = f"He apuntado que {sujeto.name} "
        if kilos:
            content += f"pesa {int(kilos)} kilos"
            if gramos:
                content += f" {int(gramos)} gramos"
        elif centimetros:
            content += f"mide {int(centimetros)} centimetros"
        elif mililitros:
            content += f"ha tomado {int(mililitros)} milititros"
        elif grados:
            content += f"está a {int(gramos)} grados"
            if decimas:
                content += f" y {int(decimas)} décimas"
        else:
            pass
        content += "."

        self.content=dict(
            payload=dict(
                google=dict(
                    expectUserResponse=True,
                    richResponse=dict(
                        items=[
                            dict(
                                simpleResponse=dict(
                                    textToSpeech=content
                                )
                            )
                        ]
                    )
                )
            )
        )

    def to_send(self):
        return self.content



class ApunteResponse(BaseModel):
    payload: dict
