from moviepy.editor import VideoFileClip, CompositeVideoClip, concatenate_videoclips, vfx

# ------------------- AVAILABLE TRANSITIONS -------------------
available_transitions = ["fade", "crossfade", "slide", "zoom", "rotate", "blur", "mirror"]

# ------------------------ ASK USER -------------------------
print("Available transitions:")
for i, t in enumerate(available_transitions, 1):
    print(f"{i}. {t}")

choice = input("Enter the transition type (or number): ").strip().lower()

# Support both name or number
if choice.isdigit():
    index = int(choice) - 1
    if 0 <= index < len(available_transitions):
        transition_type = available_transitions[index]
    else:
        print("Invalid number, defaulting to 'fade'")
        transition_type = "fade"
elif choice in available_transitions:
    transition_type = choice
else:
    print("Invalid input, defaulting to 'fade'")
    transition_type = "fade"

transition_duration = 1  # seconds

# -------------------- LOAD CLIPS ------------------------
clip1 = VideoFileClip("video1.mp4")
clip2 = VideoFileClip("video2.mp4")
clip3 = VideoFileClip("v3.mp4")
clips = [clip1, clip2, clip3]

# ------------------ TRANSITION FUNCTIONS ----------------
def apply_transition(clip_a, clip_b, t_type, duration):
    if t_type == "fade":
        return concatenate_videoclips([clip_a.fadeout(duration), clip_b.fadein(duration)])
    
    elif t_type == "crossfade":
        # Fix: Using concatenate_videoclips instead of the + operator
        return concatenate_videoclips([clip_a.crossfadeout(duration), clip_b.crossfadein(duration)])
    
    elif t_type == "slide":
        clip_b = clip_b.set_start(clip_a.duration - duration).set_position(
            lambda t: ('center', int(clip_b.h * (1 - t / duration))) if t < duration else 'center'
        )
        return CompositeVideoClip([clip_a, clip_b]).set_duration(clip_a.duration + clip_b.duration - duration)

    elif t_type == "zoom":
        zoom_b = clip_b.fx(vfx.resize, lambda t: 1 + 0.02 * t).crossfadein(duration)
        return concatenate_videoclips([clip_a.crossfadeout(duration), zoom_b], method="compose")
    
    elif t_type == "rotate":
        rot_b = clip_b.fx(vfx.rotate, lambda t: t * 30).crossfadein(duration)
        return concatenate_videoclips([clip_a.crossfadeout(duration), rot_b], method="compose")
    
    elif t_type == "blur":
        blur_a = clip_a.fx(vfx.gaussian_blur, radius=5).fadeout(duration)
        blur_b = clip_b.fx(vfx.gaussian_blur, radius=5).fadein(duration)
        return concatenate_videoclips([blur_a, blur_b])
    
    elif t_type == "mirror":
        mirror_b = clip_b.fx(vfx.mirror_x).fadein(duration)
        return concatenate_videoclips([clip_a.fadeout(duration), mirror_b])
    
    else:
        print(f"Unknown transition type: {t_type}, defaulting to fade.")
        return concatenate_videoclips([clip_a.fadeout(duration), clip_b.fadein(duration)])

# ------------------- APPLY TRANSITIONS ------------------
final_clip = clips[0]
for i in range(1, len(clips)):
    final_clip = apply_transition(final_clip, clips[i], transition_type, transition_duration)

# -------------------- EXPORT FINAL ----------------------
output_filename = f"final_video_{transition_type}_transition.mp4"
final_clip.write_videofile(output_filename, fps=24)
