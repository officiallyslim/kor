from src.global_src.global_channel_id import (
    farm_queue_channel_id,
    industrial_queue_channel_id,
    pixel_art_queue_channel_id,
    shop_queue_channel_id,
    structure_queue_channel_id,
)
from src.global_src.global_emojis import smile_pixel_emoji
from src.global_src.global_path import (
    farm_dm_embed_path,
    farm_welcome_embed_path,
    industrial_dm_embed_path,
    industrial_welcome_embed_path,
    pixel_art_dm_embed_path,
    pixel_art_welcome_embed_path,
    shop_dm_embed_path,
    shop_welcome_embed_path,
    strucure_dm_embed_path,
    strucure_welcome_embed_path,
    expo_demo_dm_embed_path,
    expo_demo_welcome_embed_path
)
from src.global_src.global_roles import (
    farm_role_id,
    industrial_role_id,
    pixel_art_role_id,
    shop_role_id,
    structure_role_id,
    expo_role_id
)

ticket_type_dict = {
    "👾Request a Pixel Art Builder👾": {
        "type": "pixel_art",
        "button_label": "Pixel Art",
        "emoji": smile_pixel_emoji,
        "role_id": pixel_art_role_id,
        "category_id": 1151613273200930948,
        "dm_embed_path": pixel_art_dm_embed_path,
        "welcome_embed_path": pixel_art_welcome_embed_path,
        "short_name": "pixel",
        "queue_channel_id": pixel_art_queue_channel_id,
    },
    "🧑‍🌾Request a Farm Builder🧑‍🌾": {
        "type": "farm",
        "button_label": "Farm",
        "emoji": "🧑‍🌾",
        "role_id": farm_role_id,
        "category_id": 1151613274589253745,
        "dm_embed_path": farm_dm_embed_path,
        "welcome_embed_path": farm_welcome_embed_path,
        "short_name": "farm",
        "queue_channel_id": farm_queue_channel_id,
    },
    "🏠Request a Structure Builder🏠": {
        "type": "structure",
        "button_label": "Structure",
        "emoji": "🏠",
        "role_id": structure_role_id,
        "category_id": 1151613279458828439,
        "dm_embed_path": strucure_dm_embed_path,
        "welcome_embed_path": strucure_welcome_embed_path,
        "short_name": "structure",
        "queue_channel_id": structure_queue_channel_id,
    },
    "🏭Request a Industrial Builder🏭": {
        "type": "industrial",
        "button_label": "Industrial",
        "emoji": "🏭",
        "role_id": industrial_role_id,
        "category_id": 1151613276510244974,
        "dm_embed_path": industrial_dm_embed_path,
        "welcome_embed_path": industrial_welcome_embed_path,
        "short_name": "industrial",
        "queue_channel_id": industrial_queue_channel_id,
    },
    "🛒Request a Shop Builder🛒": {
        "type": "shop",
        "button_label": "Shop",
        "emoji": "🛒",
        "role_id": shop_role_id,
        "category_id": 1151613278515118232,
        "dm_embed_path": shop_dm_embed_path,
        "welcome_embed_path": shop_welcome_embed_path,
        "short_name": "shop",
        "queue_channel_id": shop_queue_channel_id,
    },
    "⚒️Request an Expo/Demo worker⚒️": {
        "type": "expo_demo",
        "button_label": "Expo/Demo",
        "emoji": "⚒️",
        "role_id": expo_role_id,
        "category_id": 1151613277491695626,
        "dm_embed_path": expo_demo_dm_embed_path,
        "welcome_embed_path": expo_demo_welcome_embed_path,
        "short_name": "shop",
        "queue_channel_id": shop_queue_channel_id,
    }
}