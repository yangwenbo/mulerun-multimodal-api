"""
UI Visibility Control Handlers
"""
import gradio as gr

from config import MODELS


def update_param_visibility(model_key: str):
    """Update parameter visibility based on selected model"""
    if not model_key or model_key not in MODELS:
        return [gr.update(visible=False)] * 25  # Updated count for new URL fields

    model_config = MODELS[model_key]
    params = model_config["params"]

    updates = []

    # prompt
    if "prompt" in params:
        prompt_label = params["prompt"].get("label", "Prompt")
        updates.append(gr.update(visible=True, label=prompt_label))
    else:
        updates.append(gr.update(visible=False))

    # negative_prompt
    if "negative_prompt" in params:
        neg_prompt_label = params["negative_prompt"].get("label", "Negative Prompt")
        updates.append(gr.update(visible=True, label=neg_prompt_label))
    else:
        updates.append(gr.update(visible=False))

    # image (single image) - hide if model supports multi_image
    if "image" in params and not model_config.get("multi_image"):
        image_label = params["image"].get("label", "Input Image")
        updates.append(gr.update(visible=True, label=image_label))
        # image_url - show alongside single image upload
        updates.append(gr.update(visible=True))
    else:
        updates.append(gr.update(visible=False))
        updates.append(gr.update(visible=False))

    # multi_images (multiple images) - show if model supports multi_image
    if "image" in params and model_config.get("multi_image"):
        image_label = params["image"].get("label", "Input Images")
        max_images = model_config.get("max_images", 10)
        updates.append(gr.update(visible=True, label=f"{image_label} (最多{max_images}张)"))
        # multi_images_url - show alongside multi image upload
        updates.append(gr.update(visible=True))
    else:
        updates.append(gr.update(visible=False))
        updates.append(gr.update(visible=False))

    # model_name / model (skip hidden type)
    has_model = ("model_name" in params or "model" in params)
    model_param = params.get("model_name") or params.get("model") or {}
    if has_model and model_param.get("type") != "hidden":
        choices = model_param.get("options", [])
        default = model_param.get("default", "")
        label = model_param.get("label", "Model Version")
        updates.append(gr.update(visible=True, choices=choices, value=default, label=label))
    else:
        updates.append(gr.update(visible=False))

    # mode
    if "mode" in params:
        label = params["mode"].get("label", "Mode")
        updates.append(gr.update(visible=True, choices=params["mode"]["options"], value=params["mode"]["default"], label=label))
    else:
        updates.append(gr.update(visible=False))

    # aspect_ratio
    if "aspect_ratio" in params:
        label = params["aspect_ratio"].get("label", "Aspect Ratio")
        updates.append(gr.update(visible=True, choices=params["aspect_ratio"]["options"], value=params["aspect_ratio"]["default"], label=label))
    else:
        updates.append(gr.update(visible=False))

    # duration
    if "duration" in params:
        label = params["duration"].get("label", "Duration")
        updates.append(gr.update(visible=True, choices=params["duration"]["options"], value=params["duration"]["default"], label=label))
    else:
        updates.append(gr.update(visible=False))

    # resolution (veo3, wan2.5-i2v)
    if "resolution" in params:
        label = params["resolution"].get("label", "Resolution")
        updates.append(gr.update(visible=True, choices=params["resolution"]["options"], value=params["resolution"]["default"], label=label))
    else:
        updates.append(gr.update(visible=False))

    # size (sora, wan2.5-t2v, wan2.5-t2i)
    if "size" in params:
        label = params["size"].get("label", "Size")
        updates.append(gr.update(visible=True, choices=params["size"]["options"], value=params["size"]["default"], label=label))
    else:
        updates.append(gr.update(visible=False))

    # seconds (sora)
    if "seconds" in params:
        label = params["seconds"].get("label", "Seconds")
        updates.append(gr.update(visible=True, choices=params["seconds"]["options"], value=params["seconds"]["default"], label=label))
    else:
        updates.append(gr.update(visible=False))

    # cfg_scale
    if "cfg_scale" in params:
        label = params["cfg_scale"].get("label", "CFG Scale")
        updates.append(gr.update(visible=True, value=params["cfg_scale"]["default"], label=label))
    else:
        updates.append(gr.update(visible=False))

    # video_type (midjourney)
    if "video_type" in params:
        label = params["video_type"].get("label", "Video Type")
        updates.append(gr.update(visible=True, choices=params["video_type"]["options"], value=params["video_type"]["default"], label=label))
    else:
        updates.append(gr.update(visible=False))

    # audio (wan2.5)
    if "audio" in params:
        updates.append(gr.update(visible=True, choices=params["audio"]["options"], value=params["audio"]["default"], label=params["audio"].get("label", "Audio")))
    else:
        updates.append(gr.update(visible=False))

    # audio_url (wan2.5)
    if "audio_url" in params:
        updates.append(gr.update(visible=True, label=params["audio_url"].get("label", "Audio URL")))
    else:
        updates.append(gr.update(visible=False))

    # prompt_extend (wan2.5)
    if "prompt_extend" in params:
        updates.append(gr.update(visible=True, choices=params["prompt_extend"]["options"], value=params["prompt_extend"]["default"], label=params["prompt_extend"].get("label", "Prompt Extend")))
    else:
        updates.append(gr.update(visible=False))

    # seed (wan2.5)
    if "seed" in params:
        updates.append(gr.update(visible=True, label=params["seed"].get("label", "Seed")))
    else:
        updates.append(gr.update(visible=False))

    # n (wan2.5 t2i - number of images)
    if "n" in params:
        updates.append(gr.update(visible=True, choices=params["n"]["options"], value=params["n"]["default"], label=params["n"].get("label", "Number of Images")))
    else:
        updates.append(gr.update(visible=False))

    # shot_type (wan2.6 t2v)
    if "shot_type" in params:
        updates.append(gr.update(visible=True, choices=params["shot_type"]["options"], value=params["shot_type"]["default"], label=params["shot_type"].get("label", "Shot Type")))
    else:
        updates.append(gr.update(visible=False))

    # last_frame (veo3)
    if "last_frame" in params:
        last_frame_label = params["last_frame"].get("label", "Last Frame")
        updates.append(gr.update(visible=True, label=last_frame_label))
        # last_frame_url - show alongside last_frame upload
        updates.append(gr.update(visible=True))
    else:
        updates.append(gr.update(visible=False))
        updates.append(gr.update(visible=False))

    # reference_images (veo3)
    if "reference_images" in params:
        ref_images_label = params["reference_images"].get("label", "Reference Images")
        max_images = params["reference_images"].get("max_images", 3)
        updates.append(gr.update(visible=True, label=f"{ref_images_label} (最多{max_images}张)"))
        # reference_images_url - show alongside reference_images upload
        updates.append(gr.update(visible=True))
    else:
        updates.append(gr.update(visible=False))
        updates.append(gr.update(visible=False))

    return updates
