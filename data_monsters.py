# data_monsters.py

STRATEGY_MONSTERS = [
    {"name": "会計デーモン", "category": "財務・会計", "dialogue": "損益分岐点なんて知るわけない！", "hp": 20},
    {"name": "法律スライム", "category": "法務・知財", "dialogue": "著作権？そんなの無視だ！", "hp": 20},
    {"name": "戦略ゴブリン", "category": "経営戦略・SWOT", "dialogue": "PPMだと？食べ物の話か？", "hp": 20},
    {"name": "DXリッチ", "category": "DX・AI・生成AI", "dialogue": "デジタル変革？古い人間め！", "hp": 20},
    {"name": "システム魔将", "category": "ITガバナンス・システム戦略", "dialogue": "ITガバナンスは俺が支配する！", "hp": 20},
]
STRATEGY_BOSS = {"name": "ビジネス・デーモン", "category": "ストラテジ総合", "dialogue": "全ての経営知識を闇に葬ってやる！", "hp": 50, "is_boss": True}

MANAGEMENT_MONSTERS = [
    {"name": "WBSウルフ", "category": "プロジェクトマネジメント", "dialogue": "スケジュールを食い荒らしてやる！", "hp": 20},
    {"name": "アジャイル・ゾンビ", "category": "開発手法", "dialogue": "スプリント？走れるわけない！", "hp": 20},
    {"name": "SLAシャドウ", "category": "サービスマネジメント・ITIL", "dialogue": "SLAの約束なんて破ってやる！", "hp": 20},
    {"name": "監査ナイトメア", "category": "システム監査・リスク管理", "dialogue": "監査報告書を燃やしてやる！", "hp": 20},
]
MANAGEMENT_BOSS = {"name": "プロジェクト・トロール", "category": "マネジメント総合", "dialogue": "このプロジェクト、永遠に終わらせん！", "hp": 50, "is_boss": True}

TECHNOLOGY_MONSTERS = [
    {"name": "TCP/Iピラニア", "category": "ネットワーク", "dialogue": "パケットを全部食ってやる！", "hp": 20},
    {"name": "ランサムウェア", "category": "セキュリティ（マルウェア）", "dialogue": "データを暗号化した。身代金を払え！", "hp": 20},
    {"name": "SQLインジェクター", "category": "データベース", "dialogue": "DROP TABLE students; -- ハハハ！", "hp": 20},
    {"name": "2進数バグ", "category": "基礎理論・アルゴリズム", "dialogue": "10進数しか知らないくせに！", "hp": 20},
    {"name": "ゼロトラスト・ハッカー", "category": "最新セキュリティ", "dialogue": "信頼なんて幻想だ！侵入するぞ！", "hp": 20},
]
TECHNOLOGY_BOSS = {"name": "サイバー・ゴーレム", "category": "テクノロジ総合", "dialogue": "全てのシステムを支配するサイバー攻撃を受けるがいい！", "hp": 50, "is_boss": True}

FINAL_DUNGEON_MONSTERS = [
    {"name": "混沌の侍女", "category": "全分野ランダム", "dialogue": "3分野すべての知識がなければ通さぬ！", "hp": 30},
    {"name": "データリーパー", "category": "全分野ランダム", "dialogue": "お前の記憶を根こそぎ奪ってやる！", "hp": 30},
]
FINAL_BOSS = {"name": "マルウェア・ローグ", "category": "全分野総合", "dialogue": "ITパスポートの知識など、俺の前では無意味だ！デジタルリアルムは我が支配下に置く！", "hp": 100, "is_boss": True}

def get_monsters_for_dungeon(dungeon_id):
    if dungeon_id == "strategy":
        return STRATEGY_MONSTERS, STRATEGY_BOSS
    elif dungeon_id == "management":
        return MANAGEMENT_MONSTERS, MANAGEMENT_BOSS
    elif dungeon_id == "technology":
        return TECHNOLOGY_MONSTERS, TECHNOLOGY_BOSS
    elif dungeon_id == "final":
        return FINAL_DUNGEON_MONSTERS, FINAL_BOSS
    return [], None
