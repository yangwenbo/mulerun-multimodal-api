"""
UI Visibility Control Handlers
"""
import gradio as gr

from config import MODELS


def update_param_visibility(model_key: str):
    """Update parameter visibility based on selected model.

    Output order (28 items):
    prompt, negative_prompt,
    image, image_url,
    multi_images, multi_images_url,
    model_name, mode, aspect_ratio, duration, duration_int,
    resolution, size, seconds, cfg_scale,
    video_type, audio, audio_url, prompt_extend,
    seed, n_images, multi_shot, shot_type,
    multi_prompt,
    last_frame, last_frame_url,
    reference_images, reference_images_url
    """
    if not model_key or model_key not in MODELS:
        return [gr.update(visible=False)] * 28

    model_config = MODELS[model_key]
    params = model_config["params"]

    updates = []

    # prompt: V3 models start hidden when multi_shot default is "false" — still show it,
    # the multi_shot.change event will handle toggling.
    if "prompt" in params:
        prompt_label = params["prompt"].get("label", "Prompt")
        updates.append(gr.update(visible=True, label=prompt_label))
    else:
        updates.append(gr.update(visible=False))

    if "negative_prompt" in params:
        neg_prompt_label = params["negative_prompt"].get("label", "Negative Prompt")
        updates.append(gr.update(visible=True, label=neg_prompt_label))
    else:
        updates.append(gr.update(visible=False))

    if "image" in params and not model_config.get("multi_image"):
        image_label = params["image"].get("label", "Input Image")
        updates.append(gr.update(visible=True, label=image_label))
        updates.append(gr.update(visible=True))
    else:
        updates.append(gr.update(visible=False))
        updates.append(gr.update(visible=False))

    if "image" in params and model_config.get("multi_image"):
        image_label = params["image"].get("label", "Input Images")
        max_images = model_config.get("max_images", 10)
        updates.append(gr.update(visible=True, label=f"{image_label} (最多{max_images}张)"))
        updates.append(gr.update(visible=True))
    else:
        updates.append(gr.update(visible=False))
        updates.append(gr.update(visible=False))

    has_model = ("model_name" in params or "model" in params)
    model_param = params.get("model_name") or params.get("model") or {}
    if has_model and model_param.get("type") != "hidden":
        choices = model_param.get("options", [])
        default = model_param.get("default", "")
        label = model_param.get("label", "Model Version")
        updates.append(gr.update(visible=True, choices=choices, value=default, label=label))
    else:
        updates.append(gr.update(visible=False))

    if "mode" in params:
        label = params["mode"].get("label", "Mode")
        updates.append(gr.update(visible=True, choices=params["mode"]["options"], value=params["mode"]["default"], label=label))
    else:
        updates.append(gr.update(visible=False))

    if "aspect_ratio" in params:
        label = params["aspect_ratio"].get("label", "Aspect Ratio")
        updates.append(gr.update(visible=True, choices=params["aspect_ratio"]["options"], value=params["aspect_ratio"]["default"], label=label))
    else:
        updates.append(gr.update(visible=False))

    if "duration" in params:
        label = params["duration"].get("label", "Duration")
        updates.append(gr.update(visible=True, choices=params["duration"]["options"], value=params["duration"]["default"], label=label))
    else:
        updates.append(gr.update(visible=False))

    if "duration_int" in params:
        duration_config = params["duration_int"]
        default_val = duration_config.get("default", 5)
        min_val = duration_config.get("min", 3)
        max_val = duration_config.get("max", 15)
        label = duration_config.get("label", "Duration (seconds)")
        updates.append(gr.update(visible=True, value=default_val, minimum=min_val, maximum=max_val, label=label))
    else:
        updates.append(gr.update(visible=False))

    if "resolution" in params:
        label = params["resolution"].get("label", "Resolution")
        updates.append(gr.update(visible=True, choices=params["resolution"]["options"], value=params["resolution"]["default"], label=label))
    else:
        updates.append(gr.update(visible=False))

    if "size" in params:
        label = params["size"].get("label", "Size")
        updates.append(gr.update(visible=True, choices=params["size"]["options"], value=params["size"]["default"], label=label))
    else:
        updates.append(gr.update(visible=False))

    if "seconds" in params:
        label = params["seconds"].get("label", "Seconds")
        updates.append(gr.update(visible=True, choices=params["seconds"]["options"], value=params["seconds"]["default"], label=label))
    else:
        updates.append(gr.update(visible=False))

    if "cfg_scale" in params:
        label = params["cfg_scale"].get("label", "CFG Scale")
        updates.append(gr.update(visible=True, value=params["cfg_scale"]["default"], label=label))
    else:
        updates.append(gr.update(visible=False))

    if "video_type" in params:
        label = params["video_type"].get("label", "Video Type")
        updates.append(gr.update(visible=True, choices=params["video_type"]["options"], value=params["video_type"]["default"], label=label))
    else:
        updates.append(gr.update(visible=False))

    # audio 组件同时用于 "audio" 和 "sound" 参数
    if "audio" in params:
        updates.append(gr.update(visible=True, choices=params["audio"]["options"], value=params["audio"]["default"], label=params["audio"].get("label", "Audio")))
    elif "sound" in params:
        updates.append(gr.update(visible=True, choices=params["sound"]["options"], value=params["sound"]["default"], label=params["sound"].get("label", "Sound")))
    else:
        updates.append(gr.update(visible=False))

    if "audio_url" in params:
        updates.append(gr.update(visible=True, label=params["audio_url"].get("label", "Audio URL")))
    else:
        updates.append(gr.update(visible=False))

    if "prompt_extend" in params:
        updates.append(gr.update(visible=True, choices=params["prompt_extend"]["options"], value=params["prompt_extend"]["default"], label=params["prompt_extend"].get("label", "Prompt Extend")))
    else:
        updates.append(gr.update(visible=False))

    if "seed" in params:
        updates.append(gr.update(visible=True, label=params["seed"].get("label", "Seed")))
    else:
        updates.append(gr.update(visible=False))

    if "n" in params:
        updates.append(gr.update(visible=True, choices=params["n"]["options"], value=params["n"]["default"], label=params["n"].get("label", "Number of Images")))
    else:
        updates.append(gr.update(visible=False))

    if "multi_shot" in params:
        updates.append(gr.update(visible=True, choices=params["multi_shot"]["options"], value=params["multi_shot"]["default"], label=params["multi_shot"].get("label", "Multi Shot")))
    else:
        updates.append(gr.update(visible=False))

    if "shot_type" in params:
        updates.append(gr.update(visible=True, choices=params["shot_type"]["options"], value=params["shot_type"]["default"], label=params["shot_type"].get("label", "Shot Type")))
    else:
        updates.append(gr.update(visible=False))

    # multi_prompt: only visible when model has multi_shot AND default is "true"
    # In practice, default is "false", so hidden initially; toggled by multi_shot.change event.
    if "multi_shot" in params:
        multi_shot_default = params["multi_shot"].get("default", "false")
        updates.append(gr.update(visible=(multi_shot_default == "true"), value=""))
    else:
        updates.append(gr.update(visible=False))

    if "last_frame" in params:
        last_frame_label = params["last_frame"].get("label", "Last Frame")
        updates.append(gr.update(visible=True, label=last_frame_label))
        updates.append(gr.update(visible=True))
    else:
        updates.append(gr.update(visible=False))
        updates.append(gr.update(visible=False))

    if "reference_images" in params:
        ref_images_label = params["reference_images"].get("label", "Reference Images")
        max_images = params["reference_images"].get("max_images", 3)
        updates.append(gr.update(visible=True, label=f"{ref_images_label} (最多{max_images}张)"))
        updates.append(gr.update(visible=True))
    else:
        updates.append(gr.update(visible=False))
        updates.append(gr.update(visible=False))

    return updates


def update_multi_shot(multi_shot_value: str):
    """Toggle prompt / multi_prompt visibility when multi_shot dropdown changes.

    When multi_shot=true, default shot_type is "customize", so show multi_prompt.
    When multi_shot=false, show prompt only.

    Returns: (prompt_update, multi_prompt_update)
    """
    is_multi = (multi_shot_value == "true")
    if not is_multi:
        # single-shot: show prompt, hide multi_prompt
        return gr.update(visible=True), gr.update(visible=False)
    else:
        # multi-shot default is "customize" → hide prompt, show multi_prompt
        return gr.update(visible=False), gr.update(visible=True)


def update_shot_type(shot_type_value: str, multi_shot_value: str):
    """Toggle prompt / multi_prompt visibility when shot_type changes.

    Only meaningful when multi_shot=true:
    - customize → hide prompt, show multi_prompt
    - intelligence → show prompt, hide multi_prompt

    When multi_shot=false, always show prompt regardless of shot_type.

    Returns: (prompt_update, multi_prompt_update)
    """
    is_multi = (multi_shot_value == "true")
    if not is_multi:
        return gr.update(visible=True), gr.update(visible=False)
    is_intelligence = (shot_type_value == "intelligence")
    return gr.update(visible=is_intelligence), gr.update(visible=not is_intelligence)
