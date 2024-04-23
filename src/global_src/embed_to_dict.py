def embed_to_dict(embed):
    embed_dict = {
        "title": embed.title,
        "description": embed.description,
        "color": embed.color.value if embed.color else None,
        "fields": [{"name": field.name, "value": field.value, "inline": field.inline} for field in embed.fields],
    }

    if embed.footer:
        embed_dict["footer"] = {"text": embed.footer.text}
    if embed.image:
        embed_dict["image"] = {"url": embed.image.url}
    if embed.thumbnail:
        embed_dict["thumbnail"] = {"url": embed.thumbnail.url}

    return embed_dict