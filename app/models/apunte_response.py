from pydantic import BaseModel


class Answer:
    def __init__(self, kind = '', sujeto = None, **kwargs):
        if kind == 'location':
            if kwargs['location'] is not None:
                content = f"{sujeto.name} {'va en coche cerca de' if sujeto.latlng_car else 'está en'} {kwargs['location']}."
            else:
                content = f"Ahora mismo no se dónde está {sujeto.name}."
        elif kind == 'peso':
            content = f"He apuntado que {sujeto.name} pesa {int(kwargs['kilos'])} kilos"
            if kwargs['gramos']:
                content += f" {int(kwargs['gramos'])} gramos."
            else:
                content += '.'
        elif kind == 'altura':
            content = f"He apuntado que mide {int(kwargs['centimetros'])} centimetros."
        elif kind == 'toma':
            content = f"He apuntado que ha tomado {int(kwargs['mililitros'])} milititros."
        elif kind == 'temperatura':
            content = f"He apuntado que está a {int(kwargs['grados'])} grados"
            if kwargs['decimas']:
                content += f" y {int(kwargs['decimas'])} décimas"
            else:
                content += '.'
        else:
            content = "No te he entendido. Puedes repetir, por favor?"

        self.content=dict(
            payload=dict(
                google=dict(
                    expectUserResponse=False,
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


class BasicCard:
    def __init__(self, content, title, button_title, button_url, image_text, image_url):
        self.content=dict(
            payload=dict(
                google=dict(
                    expectUserResponse=False,
                    richResponse=dict(
                        items=[
                            dict(
                                simpleResponse=dict(
                                    textToSpeech=content
                                )
                            ),
                            dict(
                                basicCard=dict(
                                    title=title,
                                    buttons=[
                                        dict(
                                            title=button_title,
                                            openUrlAction=dict(
                                                url=button_url
                                            )
                                        )
                                    ],
                                    formattedText=image_text,
                                    image=dict(
                                        url=image_url,
                                        accessibilityText=""
                                    ),
                                ),
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
