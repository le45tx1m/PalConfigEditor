from flask import Flask, render_template, request
import subprocess
import shutil
import os
import time
import psutil
app = Flask(__name__)

###############################################
################ 修改此部分 ####################
# 配置文件路径
ini_file_path = r'C:\Program Files\PalServer\steam\steamapps\common\PalServer\Pal\Saved\Config\WindowsServer\PalWorldSettings.ini'
# 存档的文件夹路径
save_game_folder_path = r'C:\Program Files\PalServer\steam\steamapps\common\PalServer\Pal\Saved\SaveGames'
# PalServer路径
new_process_command = [r'C:\Program Files\PalServer\steam\steamapps\common\PalServer\PalServer.exe']
cwd_path = r'C:\Program Files\PalServer\steam\steamapps\common\PalServer'
# 进程名称
process_name = 'PalServer-Win64-Test-Cmd.exe'
###############################################

# 中文翻译字典，根据实际需要进行更新
translation_dict = {
    '(Difficulty': '难度',
    'DayTimeSpeedRate': '白天流逝速度',
    'NightTimeSpeedRate': '夜间流逝速度',
    'ExpRate': '经验值倍率',
    'PalCaptureRate': '帕鲁捕获概率倍率',
    'PalSpawnNumRate': '帕鲁出现倍率',
    'PalDamageRateAttack': '帕鲁攻击伤害倍率',
    'PalDamageRateDefense': '帕鲁承受伤害倍率',
    'PlayerDamageRateAttack': '玩家攻击伤害倍率',
    'PlayerDamageRateDefense': '玩家承受伤害倍率',
    'PlayerStomachDecreaceRate': '玩家饱食度降低倍率',
    'PlayerStaminaDecreaceRate': '玩家耐力降低倍率',
    'PlayerAutoHPRegeneRate': '玩家生命值自然回复倍率',
    'PlayerAutoHpRegeneRateInSleep': '玩家睡眠时生命值回复倍率',
    'PalStomachDecreaceRate': '帕鲁饱食度降低倍率',
    'PalStaminaDecreaceRate': '帕鲁耐力降低倍率',
    'PalAutoHPRegeneRate': '帕鲁生命值自然回复倍率',
    'PalAutoHpRegeneRateInSleep': '帕鲁睡眠时生命值回复倍率',
    'BuildObjectDamageRate': '对建筑伤害倍率',
    'BuildObjectDeteriorationDamageRate': '建筑物的劣化速度倍率',
    'CollectionDropRate': '道具采集倍率',
    'CollectionObjectHpRate': '可采集物品生命值倍率',
    'CollectionObjectRespawnSpeedRate': '可采集物品刷新间隔',
    'EnemyDropItemRate': '道具掉落量倍率',
    'DeathPenalty': '死亡惩罚 None=不掉落如何东西 Item=掉落装备以外的道具 ItemAndEquipment=掉落所有道具 All=掉落所有道具及队伍内帕鲁',
    'GuildPlayerMaxNum': '公会最大玩家人数',
    'PalEggDefaultHatchingTime': '巨大蛋孵化所需时间(时)/其它蛋也会改变相应孵化时间',
    'ServerPlayerMaxNum': '可以加入服务器的最大人数',
    'ServerName': '服务器名称',
    'ServerDescription': '服务器描述',
    'AdminPassword': '设置管理员密码',
    'ServerPassword': '设置服务器密码',
    'PublicPort': '开放端口',
    'PublicIP': '公网IP',
    'RCONEnabled': '启用RCON',
    'RCONPort': 'RCON端口号',
    'bEnablePlayerToPlayerDamage': '启用玩家对玩家伤害',
    'bEnableFriendlyFire': '启用友军伤害',
    'bEnableInvaderEnemy': '启用入侵者敌人',
    'bActiveUNKO': '活跃UNKO',
    'bEnableAimAssistPad': '启用手柄瞄准辅助',
    'bEnableAimAssistKeyboard': '启用键盘瞄准辅助',
    'DropItemMaxNum': '掉落物品最大数量',
    'DropItemMaxNum_UNKO': 'UNKO掉落物品最大数量',
    'BaseCampMaxNum': '基地营地最大数量',
    'BaseCampWorkerMaxNum': '基地工人最大数量',
    'DropItemAliveMaxHours': '掉落物品存活最大小时数',
    'bAutoResetGuildNoOnlinePlayers': '自动重置公会无在线玩家',
    'AutoResetGuildTimeNoOnlinePlayers': '无在线玩家时自动重置公会时间（小时）',
    'WorkSpeedRate': '工作速度倍率',
    'bIsMultiplay': '启用多人游戏',
    'bIsPvP': '启用PvP',
    'bCanPickupOtherGuildDeathPenaltyDrop': '可以拾取其他公会死亡惩罚物品',
    'bEnableNonLoginPenalty': '启用非登录惩罚',
    'bEnableFastTravel': '启用快速旅行',
    'bIsStartLocationSelectByMap': '启用地图选择起始位置',
    'bExistPlayerAfterLogout': '登出后存在玩家',
    'bEnableDefenseOtherGuildPlayer': '启用防守其他公会玩家',
    'CoopPlayerMaxNum': '合作玩家最大数量',
    'Region': '地区',
    'bUseAuth': '启用身份验证',
    'BanListURL': '封禁列表URL'
}

# 以'utf-8'编码方式读取PalWorldSettings.ini文件内容
with open(ini_file_path, 'r', encoding='utf-8') as file:
    ini_content = file.read()

# 获取OptionSettings中的所有配置项
option_settings_line = ini_content.split('[/Script/Pal.PalGameWorldSettings]')[1].split('\n', 1)[1].strip()
option_settings = {}
for setting in option_settings_line[15:-1].split(','):
    key, value = setting.split('=')
    option_settings[key.strip()] = value.strip()

# # 关闭指定进程
# def kill_process(process_name):
#     try:
#         # 使用 taskkill 命令关闭进程
#         subprocess.run(['taskkill', '/F', '/IM', process_name], check=True, capture_output=True)
#         print(f'Process {process_name} terminated.')
#     except subprocess.CalledProcessError as e:
#         print(f'Error terminating process {process_name}: {e.stderr.decode()}')

# 关闭指定进程
def kill_process(process_name):
    for process in psutil.process_iter(['pid', 'name']):
        if process.info['name'] == process_name:
            pid = process.info['pid']
            try:
                # 使用 terminate 方法关闭进程
                psutil.Process(pid).terminate()
                print(f'Process {process_name} with PID {pid} terminated.')
            except psutil.NoSuchProcess:
                print(f'Process {process_name} with PID {pid} not found.')


# 启动新进程
def start_process(command):
    subprocess.Popen(new_process_command, cwd=cwd_path)
    print(f'Process started with command: {command}')

# 等待一段时间确保进程关闭
def wait_for_process_to_close(process_name, timeout=10):
    start_time = time.time()
    while is_process_running(process_name):
        time.sleep(1)
        if time.time() - start_time > timeout:
            print(f'Timeout waiting for process {process_name} to close.')
            break

# 检查指定进程是否在运行
def is_process_running(process_name):
    for process in psutil.process_iter(['pid', 'name']):
        if process.info['name'] == process_name:
            return True
    return False

def restart_game_server():
    # 如果进程在运行，关闭它
    if is_process_running(process_name):
        kill_process(process_name)
        # 等待一段时间确保进程关闭
        wait_for_process_to_close(process_name)
    # 启动新进程
    start_process(new_process_command)

@app.route('/')
def index():
    # 将OptionSettings中的所有配置项、中文翻译字典传递给模板
    return render_template('index.html', option_settings=option_settings, translation_dict=translation_dict)

@app.route('/update_settings', methods=['POST'])
def update_settings():
    # 从表单中获取修改后的内容
    for key in option_settings.keys():
        updated_value = request.form.get(key)
        if updated_value is not None:
            option_settings[key] = updated_value

    # 更新OptionSettings的内容
    updated_option_settings = ",".join([f"{key}={value}" for key, value in option_settings.items()])

    # 替换原始OptionSettings中的内容
    updated_content = ini_content.replace(option_settings_line, f"OptionSettings={updated_option_settings})")

    # 将修改后的内容保存到PalWorldSettings.ini文件
    with open(ini_file_path, 'w', encoding='utf-8') as file:
        file.write(updated_content)

    # 执行
    restart_game_server()

    return render_template('index.html', option_settings=option_settings, translation_dict=translation_dict, message='配置已更新!')

@app.route('/delete_folder', methods=['POST'])
def delete_folder():

    if os.path.exists(save_game_folder_path):
        try:
            # 删除指定文件夹
            shutil.rmtree(save_game_folder_path)
            message = '删除成功!'
        except subprocess.CalledProcessError as e:
            message = '删除失败'
    else:
        message = '删除成功!'
        
    # 执行
    restart_game_server()

    return render_template('index.html', option_settings=option_settings, translation_dict=translation_dict, message=message)

restart_game_server()
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
