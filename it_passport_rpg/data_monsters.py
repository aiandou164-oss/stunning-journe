# data_monsters.py

LAWS_MONSTERS = [
    {"name": "測量法ゴブリン", "category": "測量法規", "dialogue": "測量法を無視する奴は俺が裁く！", "hp": 20},
    {"name": "無許可スライム", "category": "測量法規", "dialogue": "国土地理院長の承認なんて知らない！", "hp": 20},
]
LAWS_BOSS = {"name": "ルール・ゴブリン", "category": "測量法規", "dialogue": "公共測量の規則を破る気か！", "hp": 50, "is_boss": True}

TRAVERSE_MONSTERS = [
    {"name": "偏心オーク", "category": "多角測量", "dialogue": "偏心補正を間違えさせてやる！", "hp": 30},
    {"name": "閉合差ウルフ", "category": "多角測量", "dialogue": "角度の閉合差が許容範囲を超えているぞ！", "hp": 20},
]
TRAVERSE_BOSS = {"name": "トラバース・オーク", "category": "多角測量", "dialogue": "すべてのトータルステーションの座標を狂わせてやる！", "hp": 50, "is_boss": True}

GNSS_MONSTERS = [
    {"name": "マルチパス・バット", "category": "GNSS", "dialogue": "建物の反射波に惑わされるがいい！", "hp": 20},
    {"name": "サイクルスリップ星人", "category": "GNSS", "dialogue": "電波の位相を狂わせてやったぞ！", "hp": 20},
]
GNSS_BOSS = {"name": "サテライト・ゴーレム", "category": "GNSS", "dialogue": "宇宙からのGPS信号を全て遮断する！", "hp": 50, "is_boss": True}

LEVELING_MONSTERS = [
    {"name": "視準軸エラー虫", "category": "水準測量", "dialogue": "レベルの気泡がずれているぞ！", "hp": 20},
    {"name": "沈下トロル", "category": "水準測量", "dialogue": "水準点が沈下してしまった！", "hp": 20},
]
LEVELING_BOSS = {"name": "レベル・ウルフ", "category": "水準測量", "dialogue": "標高差の計算ミスでパニックになれ！", "hp": 50, "is_boss": True}

TOPOGRAPHIC_MONSTERS = [
    {"name": "等高線スネーク", "category": "地形測量", "dialogue": "主曲線と計曲線の区別がつくかな？", "hp": 20},
    {"name": "UAVファイター", "category": "地形測量", "dialogue": "ドローン測量の邪魔をしてやる！", "hp": 20},
]
TOPOGRAPHIC_BOSS = {"name": "コンター・ドラゴン", "category": "地形測量", "dialogue": "大地の起伏を全て平坦にしてやる！", "hp": 60, "is_boss": True}

PHOTOGRAMMETRY_MONSTERS = [
    {"name": "標定点泥棒", "category": "写真測量", "dialogue": "対空標識を持っていってやったぞ！", "hp": 20},
    {"name": "オーバーラップ鳥", "category": "写真測量", "dialogue": "重複度の計算を狂わせてやる！", "hp": 20},
]
PHOTOGRAMMETRY_BOSS = {"name": "エアリアル・キメラ", "category": "写真測量", "dialogue": "空中からの立体視を不可能にしてやる！", "hp": 60, "is_boss": True}

MAP_COMPILATION_MONSTERS = [
    {"name": "図式ゴースト", "category": "地図編集", "dialogue": "地図記号のルールを忘れたのか？", "hp": 20},
    {"name": "縮尺ミスゾンビ", "category": "地図編集", "dialogue": "1万分の1か2万5千分の1か分からなくしてやる！", "hp": 20},
]
MAP_COMPILATION_BOSS = {"name": "エディット・デーモン", "category": "地図編集", "dialogue": "この世界の地図を白紙に戻してやる！", "hp": 50, "is_boss": True}

APPLIED_MONSTERS = [
    {"name": "クロソイド曲線魔人", "category": "応用測量", "dialogue": "緩和曲線の計算で頭を抱えろ！", "hp": 20},
    {"name": "用地境界デーモン", "category": "応用測量", "dialogue": "境界標なんか抜いてやる！", "hp": 20},
]
APPLIED_BOSS = {"name": "ルート・ビルダー", "category": "応用測量", "dialogue": "全ての路線と河川を俺の思い通りに曲げてやる！", "hp": 60, "is_boss": True}

FINAL_DUNGEON_MONSTERS = [
    {"name": "大地の番人", "category": "全分野ランダム", "dialogue": "すべての測量知識なくして大地の魔王には会えぬ！", "hp": 30},
    {"name": "アトラスナイト", "category": "全分野ランダム", "dialogue": "測地系の歪みに飲み込まれよ！", "hp": 30},
]
FINAL_BOSS = {"name": "大地の魔王アースクエイク", "category": "全分野総合", "dialogue": "測量士補の知識など無意味だ！世界図を無茶苦茶に引き裂いてやる！", "hp": 100, "is_boss": True}

def get_monsters_for_dungeon(dungeon_id):
    if dungeon_id == "laws": return LAWS_MONSTERS, LAWS_BOSS
    elif dungeon_id == "traverse": return TRAVERSE_MONSTERS, TRAVERSE_BOSS
    elif dungeon_id == "gnss": return GNSS_MONSTERS, GNSS_BOSS
    elif dungeon_id == "leveling": return LEVELING_MONSTERS, LEVELING_BOSS
    elif dungeon_id == "topographic": return TOPOGRAPHIC_MONSTERS, TOPOGRAPHIC_BOSS
    elif dungeon_id == "photogrammetry": return PHOTOGRAMMETRY_MONSTERS, PHOTOGRAMMETRY_BOSS
    elif dungeon_id == "map_compilation": return MAP_COMPILATION_MONSTERS, MAP_COMPILATION_BOSS
    elif dungeon_id == "applied": return APPLIED_MONSTERS, APPLIED_BOSS
    elif dungeon_id == "final": return FINAL_DUNGEON_MONSTERS, FINAL_BOSS
    
    return LAWS_MONSTERS, LAWS_BOSS  # fallback
