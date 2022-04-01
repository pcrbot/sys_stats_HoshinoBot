import platform

import hoshino
import psutil
from hoshino import Service, priv
from hoshino.util import FreqLimiter

islinux = platform.system().lower() == "linux"

if islinux:
    import distro


flmt = FreqLimiter(30)

sv = Service(
    name="系统自检",  # 功能名
    use_priv=priv.NORMAL,  # 使用权限
    manage_priv=priv.ADMIN,  # 管理权限
    visible=True,  # False隐藏
    enable_on_default=True,  # 是否默认启用
)


def human(n):
    symbols = ("K", "M", "G", "T", "P", "E", "Z", "Y")
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return "%.1f%s" % (value, s)
    return "%sB" % n


def get_platform():
    platform_info = {
        "运行平台": f"{platform.system()} {platform.version()}",
        "架构": platform.machine(),  # 这个该叫什么？  # 叫架构 (architecture)
    }
    if islinux:
        platform_info.update(
            {
                "运行平台": f"{distro.os_release_info()['name']} {distro.os_release_info()['version']}",
            }
        )
    return platform_info


def get_cpu():
    cpu_info = {
        # "CPU": platform.processor(),
        "物理CPU数": psutil.cpu_count(logical=False),
        "逻辑CPU数": psutil.cpu_count(),
        "频率": f"{psutil.cpu_freq()[0]/1000:.2f}GHz",
        "使用率": f"{psutil.cpu_percent(interval=0.2)}%（在0.2秒内）",
    }
    return cpu_info


def get_memory():
    virmem = psutil.virtual_memory()
    memory_info = {
        "总大小": human(virmem[0]),
        "已使用": f"{human(virmem[3])} ({virmem[2]}%)",
        "剩余": human(virmem[1]),
    }
    return memory_info


def get_swap():
    swapmem = psutil.swap_memory()
    swap_info = {
        "总大小": human(swapmem[0]),
        "已使用": f"{human(swapmem[1])} ({swapmem[3]}%)",
        "剩余": human(swapmem[2]),
    }
    if islinux:
        swap_info.update(
            {
                "累计I/O": f"{human(swapmem[4])} / {human(swapmem[5])}",
            }
        )
    return swap_info


def get_disk():
    disk_list = []
    disk_info = []
    for disk in psutil.disk_partitions():
        disk_list.append([disk[0], disk[1]])  # 标识，挂载点
    for disk in disk_list:
        try:
            usage = psutil.disk_usage(disk[1])
        except (PermissionError, psutil.AccessDenied):
            # 无法读取硬盘，WinServer有可能是一个光驱导致，跳过
            continue
        disk_temp = {
            "标识": disk[0],
        }
        if islinux:
            disk_temp.update({"挂载点": disk[1]})
        disk_temp.update(
            {
                "总大小": human(usage[0]),
                "已使用": f"{human(usage[1])} ({usage[3]}%)",
                "剩余": human(usage[2]),
            }
        )
        disk_info.append(disk_temp)
    return disk_info


@sv.on_fullmatch(("check", "自检", "鲁大师"), only_to_me=True)
async def sys_stats(bot, ev):
    # 冷却器检查，每群30秒CD
    if not flmt.check(ev['group_id']):
        await bot.send(ev, f"自检冷却中，请在{flmt.left_time(ev['group_id']):.2f}秒后再试~")
        return
    flmt.start_cd(ev['group_id'])
    await bot.send(ev, "正在执行自检……")
    msg = "System Info：\n"
    msg += "平台：\n"
    for key, value in get_platform().items():
        msg += f" {key}：{value}\n"
    msg += "CPU：\n"
    for key, value in get_cpu().items():
        msg += f" {key}：{value}\n"
    msg += "物理内存：\n"
    for key, value in get_memory().items():
        msg += f" {key}：{value}\n"
    msg += ("虚拟内存" if platform.system().lower()
            == "windows" else "swap") + "\n"
    for key, value in get_swap().items():
        msg += f" {key}：{value}\n"
    msg += "硬盘：\n"
    for disks in get_disk():
        for key, value in disks.items():
            msg += f" {key}：{value}\n"
    try:
        await bot.send(ev, msg)
    except:
        await bot.finish(ev, "自检结果发送失败！")
