import bisect
import math


def nearest_keyframe(target, keys):
    """最近关键帧：不超过目标时间的最后一个关键帧。"""
    keys = sorted(keys)
    if not keys:
        raise ValueError("no keyframes available")
    pos = bisect.bisect_right(keys, target)
    if pos == 0:
        return keys[0]
    return keys[pos - 1]


def decode_until(target, current):
    """从当前解码位置解码到目标所需的帧数。"""
    return max(0, target - current)


def bframe_pts(dts, reorder):
    """由解码时间戳和重排深度得到 B 帧的显示时间戳。"""
    return dts + reorder


def edit_offset(pts, edit_start):
    """编辑列表裁掉片头后，换算为以新起点计的时间戳。"""
    return pts - edit_start


def vfr_time(durations, frame):
    """按实际帧时长累计，得到第 frame 帧的显示时间。"""
    if frame <= 0:
        return 0
    return sum(durations[:frame])


def sync_audio(video_time, offset):
    """音频按视频 seek 位置同步，offset 为音画偏移。"""
    return video_time + offset


def reset_params(old, new):
    """切换到新片段时重置参数集，返回生效的新参数集。"""
    return new


def preroll(gop_length):
    """预滚帧数：按 GOP 长度取两倍，保证覆盖前向参考。"""
    return gop_length * 2


def clear_queue(frames):
    """清空 seek 前的输出队列，返回剩余帧数。"""
    clear = getattr(frames, "clear", None)
    if callable(clear):
        clear()
        return len(frames)
    if isinstance(frames, list):
        del frames[:]
        return len(frames)
    # 传入的是待清空的帧数，清空后没有残留。
    return 0


def lookup_index(index, time):
    """在索引表中查找不超过目标时间的最近条目。"""
    times = sorted(index)
    if not times:
        raise ValueError("empty index")
    pos = bisect.bisect_right(times, time)
    if pos == 0:
        return times[0]
    return times[pos - 1]


def gop_start(time, gop):
    """目标时间所在 GOP 的起点（对齐到 GOP 边界）。"""
    if gop <= 0:
        raise ValueError("gop length must be positive")
    return (time // gop) * gop


def byte_to_time(bytes, bitrate):
    """按字节偏移与码率估算时间戳。"""
    if bitrate <= 0:
        raise ValueError("bitrate must be positive")
    return bytes / bitrate


def valid_keyframe(key):
    """关键帧位置是否合法：非负且有限。"""
    if isinstance(key, bool) or not isinstance(key, (int, float)):
        return False
    return math.isfinite(key) and key >= 0


def seek_key(seed, index):
    """生成 seek 键，标识片段与索引位置。"""
    return f"{seed}:{index}"


def frame_duration(fps):
    """单帧时长（秒）。"""
    if fps <= 0:
        raise ValueError("fps must be positive")
    return 1.0 / fps
