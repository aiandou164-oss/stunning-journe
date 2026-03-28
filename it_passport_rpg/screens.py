import streamlit as st
import time
import random
from components import render_status_bar, show_nanami_message, show_akira_message, play_bgm, stop_bgm, play_hit_sfx
from data_questions import QUESTIONS
from data_monsters import get_monsters_for_dungeon

def check_level_up():
    exp = st.session_state.exp
    old_lvl = st.session_state.level
    
    thresholds = [0, 150, 400, 800, 1500, 2500, 4000, 6000, 10000, 99999]
    titles = ["見習いITエンジニア", "ITの卵", "ネットワーク見習い", "データベース探索者", "セキュリティ戦士", "ITパスポート候補生", "デジタルリアルムの英雄", "マスター・オブ・IT", "ITの神"]
    
    new_lvl = 1
    for i, t in enumerate(thresholds):
        if exp >= t:
            new_lvl = i + 1
            
    if new_lvl > 7: new_lvl = 7
    
    if new_lvl > old_lvl:
        st.session_state.level = new_lvl
        st.balloons()
        st.success(f"🎉 レベルアップ！ Lv.{new_lvl} 【{titles[new_lvl-1]}】になった！")

def show_title_screen():
    play_bgm("town")
    st.markdown('<div class="game-title">ITパスポート冒険記<br>〜デジタルの魔王を倒せ！〜</div>', unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center;'>デジタルの魔王を倒し、ITの紋章を手に入れろ！</h4>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    render_status_bar()
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⚔️ RPG冒険モード", use_container_width=True):
            st.session_state.mode = "rpg"
            st.session_state.screen = "dungeon_select"
            st.rerun()
        if st.button("🎯 弱点特訓", use_container_width=True):
            st.session_state.mode = "weak"
            st.session_state.screen = "weakness_select"
            st.rerun()
            
    with col2:
        if st.button("📝 本試験シミュレーター", use_container_width=True):
            st.session_state.mode = "exam"
            st.session_state.screen = "exam_select" 
            st.rerun()
        if st.button("📚 カテゴリ速習", use_container_width=True):
            st.session_state.mode = "category"
            st.session_state.screen = "category_select"
            st.rerun()
            
    st.divider()
    cleared = st.session_state.cleared_dungeons
    st.markdown("### 🏆 獲得した紋章")
    badges = []
    if "strategy" in cleared: badges.append("🏰 ストラテジの紋章")
    if "management" in cleared: badges.append("🌳 マネジメントの紋章")
    if "technology" in cleared: badges.append("🗼 テクノロジの紋章")
    if "final" in cleared: badges.append("👑 魔王討伐の証")
    
    if badges:
        st.markdown(" ".join(badges))
    else:
        st.markdown("まだ紋章を持っていません。")

DUNGEON_DATA = {
    "strategy_1": {"name": "ストラテジ村 🏡", "desc": "ストラテジ基礎", "boss": "ビジネス・スライム", "req_lv": 1, "domain": "strategy"},
    "strategy_2": {"name": "ストラテジ砦 🏰", "desc": "ストラテジ応用", "boss": "法務ゴブリン", "req_lv": 2, "domain": "strategy"},
    "strategy_3": {"name": "ストラテジ城 👑", "desc": "ストラテジ発展", "boss": "経営ドラゴン", "req_lv": 3, "domain": "strategy"},
    "management_1": {"name": "マネジメント森 🌳", "desc": "マネジメント基礎", "boss": "開発ウルフ", "req_lv": 2, "domain": "management"},
    "management_2": {"name": "マネジメント洞窟 🕳️", "desc": "マネジメント応用", "boss": "品質オーク", "req_lv": 3, "domain": "management"},
    "management_3": {"name": "マネジメント山 🌋", "desc": "マネジメント発展", "boss": "監査ゴーレム", "req_lv": 4, "domain": "management"},
    "technology_1": {"name": "テクノロジ塔 🗼", "desc": "テクノロジ基礎", "boss": "ネットワーク・バグ", "req_lv": 3, "domain": "technology"},
    "technology_2": {"name": "テクノロジ基地 🏭", "desc": "テクノロジ応用", "boss": "DBキメラ", "req_lv": 4, "domain": "technology"},
    "technology_3": {"name": "テクノロジ神殿 ⛩️", "desc": "テクノロジ発展", "boss": "セキュリティデーモン", "req_lv": 5, "domain": "technology"},
    "final": {"name": "魔王城", "req_lv": 5, "domain": "all"},
    "weakness": {"name": "弱点特訓道場", "req_lv": 1, "domain": "all"},
}

def show_dungeon_select():
    play_bgm("town")
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("## 🗺️ ダンジョン選択")
    with col2:
        if st.button("◀ タイトルに戻る"):
            st.session_state.screen = "title"
            st.rerun()
            
    render_status_bar()
    
    DUNGEONS = [v | {"id": k} for k, v in DUNGEON_DATA.items() if not k in ["final", "weakness"]]
    
    cols = st.columns(3)
    st_dungeons = [d for d in DUNGEONS if d['domain'] == 'strategy']
    ma_dungeons = [d for d in DUNGEONS if d['domain'] == 'management']
    te_dungeons = [d for d in DUNGEONS if d['domain'] == 'technology']
    
    for idx, d_list in enumerate([st_dungeons, ma_dungeons, te_dungeons]):
        with cols[idx]:
            st.markdown(f"### {'ストラテジ' if idx==0 else 'マネジメント' if idx==1 else 'テクノロジ'}領域")
            for d in d_list:
                with st.container():
                    st.markdown(f"#### {d['name']}")
                    st.markdown(f"推奨: Lv.{d['req_lv']} 〜 | ボス: {d['boss']}")
                    if d['id'] in st.session_state.cleared_dungeons:
                        st.success("✅ クリア済み")
                        
                    if st.session_state.level >= d["req_lv"]:
                        if st.button(f"挑む！", key=f"btn_{d['id']}", use_container_width=True):
                            setup_dungeon(d['id'], d['domain'])
                    else:
                        st.button(f"🔒 Lv.{d['req_lv']}必要", key=f"lk_{d['id']}", disabled=True, use_container_width=True)
                    st.markdown("<br>", unsafe_allow_html=True)
                
    st.divider()
    st.markdown("### 🏯 魔王城 (最終決戦)")
    main_cleared = [c for c in st.session_state.cleared_dungeons if not str(c).startswith("category") and c != "weakness" and c != "final"]
    if len(set(main_cleared)) >= 9:
        if st.button("⚔️ 魔王マルウェア・ローグに挑む", type="primary", use_container_width=True):
            setup_dungeon("final", "all")
    else:
        st.markdown(f"全9つのステージをクリアすると魔王城への道が開かれます。（現在: {len(set(main_cleared))}/9）")
        
    # Footer

def setup_dungeon(dungeon_id, domain="all"):
    st.session_state.current_dungeon = dungeon_id
    st.session_state.current_domain = domain
    
    if dungeon_id == "final" or domain == "all":
        q_pool = QUESTIONS.copy()
    else:
        mapping = {"strategy": "企業活動", "management": "システム開発", "technology": "ネットワーク"}
        q_pool = [q for q in QUESTIONS if domain in q.get("domain", "") or domain in q.get("dungeon", "") or mapping.get(domain, domain) in q.get("category", "")]
        if not q_pool: q_pool = QUESTIONS.copy()
        
    num_questions = min(10, len(q_pool))
    st.session_state.current_questions = random.sample(q_pool, num_questions)
    st.session_state.question_index = 0
    st.session_state.screen = "battle"
    st.session_state.hp = 100 
    st.session_state.combo = 0
    init_battle_state()
    st.rerun()

def init_battle_state():
    idx = st.session_state.question_index
    if idx == 0:
        st.session_state.current_mistakes = []
        
    if idx >= len(st.session_state.current_questions):
        st.session_state.screen = "dungeon_clear"
        return
        
    q = st.session_state.current_questions[idx]
    total = len(st.session_state.current_questions)
    
    boss_hits = 5 if st.session_state.current_dungeon == "final" else 3
    is_boss = (idx >= total - boss_hits) and (total >= boss_hits)
    
    if is_boss:
        if st.session_state.current_dungeon == "final":
            monster = {"name": "魔王マルウェア・ローグ", "dialogue": "我輩の知識にひれ伏すがいい！", "hp": 5}
        else:
            domain_names = {"strategy": "ビジネス", "management": "システム", "technology": "サイバー"}
            prefix = domain_names.get(st.session_state.get("current_domain", "strategy"), "謎の")
            monster = {"name": f"{prefix}ボス", "dialogue": "フハハハ、ここを通るつもりか！", "hp": 3}
    else:
        monsters, _ = get_monsters_for_dungeon("strategy") # fallback for normal monsters
        cat_monsters = [m for m in monsters if m["category"] == q.get("category")]
        monster = random.choice(cat_monsters) if cat_monsters else random.choice(monsters)
        if st.session_state.get("current_domain") == "all":
            monster = {"name": "修練のホログラム", "dialogue": "ピピピ... 仮想戦闘プログラム起動。", "hp": 1}
            
    st.session_state.battle_state = {
        "monster": monster,
        "is_boss": is_boss,
        "question": q,
        "answered": False,
        "selected_choice": None,
        "feedback": None
    }

def show_battle_screen():
    st.markdown("<span id='top-of-page'></span>", unsafe_allow_html=True)
    
    bstate = st.session_state.battle_state
    if not bstate:
        play_bgm("battle")
        init_battle_state()
        st.rerun()
        
    is_boss = bstate.get("is_boss", False)
    if is_boss:
        play_bgm("boss")
    else:
        play_bgm("battle")
        
    q = bstate["question"]
    monster = bstate["monster"]
    is_boss = bstate["is_boss"]
    idx = st.session_state.question_index
    total = len(st.session_state.current_questions)
    
    st.markdown(f"**[進捗] {idx+1} / {total}**")
    
    boss_hits = 5 if st.session_state.current_dungeon == "final" else 3
    if is_boss:
        st.markdown(f"<div class='boss-header'>⚠️ BOSS BATTLE ⚠️<br>{monster['name']}</div>", unsafe_allow_html=True)
        hits_remaining = total - idx
        st.progress(hits_remaining / boss_hits)
    else:
        st.markdown(f"### 💀 {monster['name']}")
        st.progress(1.0) 
        
    st.markdown(f"*{monster['dialogue']}*")
    st.divider()
    
    render_status_bar()
    
    st.markdown(f"**【Q】 {q['question']}**")
    
    if not bstate["answered"]:
        js = f'''
        <script>
            setTimeout(function() {{
                const el = window.parent.document.getElementById("top-of-page");
                if (el) {{ el.scrollIntoView({{behavior: "smooth", block: "start"}}); }}
            }}, 100);
            // Unique execution trigger: Q_ID {q.get('id', idx)}
        </script>
        '''
        st.components.v1.html(js, height=0, width=0)
            
        with st.form(key=f"battle_form_{q['id']}"):
            choice = st.radio("選択肢", list(q["choices"].keys()), format_func=lambda x: f"{x}. {q['choices'][x]}")
            submitted = st.form_submit_button("⚔️ 回答する", use_container_width=True)
            if submitted:
                play_hit_sfx()
                bstate["answered"] = True
                bstate["selected_choice"] = choice
                
                if choice == q["answer"]:
                    bstate["feedback"] = "correct"
                else:
                    bstate["feedback"] = "wrong"
                st.rerun()
    else:
        if bstate["feedback"] == "correct":
            st.markdown(f"<div class='correct-flash'>⚔️ 攻撃成功！ {monster['name']} にダメージ！<br>正解！</div>", unsafe_allow_html=True)
            if "score_added" not in bstate:
                if q.get("id") in st.session_state.wrong_questions:
                    st.session_state.wrong_questions.remove(q["id"])
                st.session_state.combo += 1
                pts = 100
                exp = 10
                if st.session_state.combo >= 3:
                    pts += 50
                if is_boss:
                    pts += 500
                    exp += 50
                    
                st.session_state.score += pts
                st.session_state.exp += exp
                bstate["score_added"] = True
                
        elif bstate["feedback"] == "wrong":
            req_lv = DUNGEON_DATA.get(st.session_state.current_dungeon, {}).get("req_lv", 1)
            damage = 10 * req_lv * (2 if is_boss else 1)
            
            st.markdown(f"<div class='wrong-flash'>💔 痛恨の一撃！ HP -{damage}<br>不正解…正解は「{q['answer']}」</div>", unsafe_allow_html=True)

            if "score_added" not in bstate:
                if q.get("id") not in st.session_state.wrong_questions:
                    st.session_state.wrong_questions.append(q.get("id"))
                
                if not any(m["q"]["id"] == q["id"] for m in st.session_state.get("current_mistakes", [])):
                    st.session_state.current_mistakes.append({"q": q, "choice": bstate["selected_choice"]})
                    
                st.session_state.combo = 0
                st.session_state.hp -= damage
                bstate["score_added"] = True
                
        check_level_up()
        show_nanami_message(q["explanation"])
        
        if st.session_state.hp <= 0:
            if st.button("続ける...", use_container_width=True):
                st.session_state.screen = "game_over"
                st.rerun()
        else:
            if bstate["feedback"] == "correct":
                btn_lbl = "次の問題へ ▶" if idx < total - 1 else "🎉 ダンジョンクリア！結果を見る ▶"
                if st.button(btn_lbl, type="primary", use_container_width=True):
                    st.session_state.question_index += 1
                    init_battle_state()
                    st.rerun()
            else:
                if st.button("もう一度この問題に挑む", type="primary", use_container_width=True):
                    bstate["answered"] = False
                    bstate["feedback"] = None
                    if "score_added" in bstate:
                        del bstate["score_added"]
                    st.rerun()

def show_game_over():
    stop_bgm()
    st.markdown("<h2 style='text-align: center; color: red;'>💀 アキラは力尽きた…</h2>", unsafe_allow_html=True)
    show_nanami_message("大丈夫、また挑戦しよう！間違えたところはリストアップしておいたよ！")
    
    if st.button("諦めない！もう一度挑む", type="primary", use_container_width=True):
        st.session_state.hp = 100
        st.session_state.combo = 0
        st.session_state.question_index = 0
        init_battle_state()
        st.session_state.screen = "battle"
        st.rerun()
        
    if st.button("ダンジョン選択に戻る", use_container_width=True):
        st.session_state.screen = "dungeon_select"
        st.rerun()

def show_dungeon_clear():
    play_bgm("clear")
    dungeon_id = st.session_state.current_dungeon
    if dungeon_id not in st.session_state.cleared_dungeons:
        st.session_state.cleared_dungeons.append(dungeon_id)
        st.session_state.score += 1000
        st.session_state.exp += 50
        check_level_up()
        
    st.balloons()
    st.markdown(f"<h1 style='text-align: center;'>🏆 ダンジョン攻略成功！</h1>", unsafe_allow_html=True)
    
    if st.session_state.get("current_mistakes"):
        st.markdown("### 📝 間違えた問題と解説 (見直し)")
        for i, m in enumerate(st.session_state.current_mistakes):
            q = m["q"]
            with st.expander(f"Q: {q['question']}"):
                st.markdown(f"**あなたの最初の解答**: {m['choice']}  |  **正解**: {q['answer']}")
                st.markdown(f"**解説**: {q['explanation']}")
                
        if st.button("間違えた問題をもう一度特訓する", type="primary", use_container_width=True):
            st.session_state.current_questions = [m["q"] for m in st.session_state.current_mistakes]
            st.session_state.question_index = 0
            st.session_state.current_mistakes = []
            st.session_state.hp = 100
            st.session_state.combo = 0
            init_battle_state()
            st.session_state.screen = "battle"
            st.rerun()
    else:
        st.success("✨ パーフェクトクリア！ノーミスで素晴らしい知識です！")
        
    st.divider()
    if dungeon_id == "final":
        show_nanami_message("すごい！魔王を倒したよ！デジタルリアルム王国を救ってくれてありがとう！")
        if st.button("グランドフィナーレへ", type="primary", use_container_width=True):
            st.session_state.screen = "finale"
            st.rerun()
    else:
        show_nanami_message("やったね！見直しが終わったら他のダンジョンも攻略しよう！")
        if st.button("ダンジョン選択に戻る", type="primary", use_container_width=True):
            st.session_state.screen = "dungeon_select"
            st.rerun()
            
def show_finale():
    play_bgm("town")
    st.snow()
    st.markdown("<h1 style='text-align: center; color: #FFD700;'>🎉 祝・ITパスポート合格レベル到達！ 🎉</h1>", unsafe_allow_html=True)
    st.markdown("### デジタルリアルム王国に平和が訪れた！")
    
    st.markdown(f"**最終スコア**: {st.session_state.score}pt")
    st.markdown(f"**最終レベル**: Lv.{st.session_state.level}")
    
    show_akira_message("ついにやったぞ！これなら本試験も怖くない！")
    show_nanami_message("本当に頑張ったね！次は『本試験シミュレーター』で実力を試してみてね！")
    
    if st.button("タイトルに戻る", type="primary", use_container_width=True):
        st.session_state.screen = "title"
        st.rerun()

def show_exam_settings():
    play_bgm("town")
    st.markdown("## 📝 本試験シミュレーター")
    st.info("本試験と同じ形式で出題します。（全100問からランダムで出題）")
    if st.button("試験開始！", type="primary", use_container_width=True):
        st.session_state.current_questions = random.sample(QUESTIONS, min(len(QUESTIONS), 100))
        st.session_state.question_index = 0
        st.session_state.exam_results = []
        st.session_state.screen = "exam"
        st.rerun()
    if st.button("戻る"):
        st.session_state.screen = "title"
        st.rerun()

def show_exam_screen():
    st.markdown("<span id='top-of-page'></span>", unsafe_allow_html=True)
    idx = st.session_state.question_index
    total = len(st.session_state.current_questions)
    
    if idx >= total:
        st.session_state.screen = "exam_result"
        st.rerun()
        
    q = st.session_state.current_questions[idx]
    
    js = f'''
    <script>
        setTimeout(function() {{
            const el = window.parent.document.getElementById("top-of-page");
            if (el) {{ el.scrollIntoView({{behavior: "smooth", block: "start"}}); }}
        }}, 100);
        // Unique execution trigger: Q_ID {q.get('id', idx)}
    </script>
    '''
    st.components.v1.html(js, height=0, width=0)

    st.markdown(f"**問題 {idx + 1} / {total}**")
    st.markdown(f"### {q['question']}")
    
    with st.form(key=f"exam_form_{q['id']}"):
        choice = st.radio("選択", list(q["choices"].keys()), format_func=lambda x: f"{x}. {q['choices'][x]}")
        sub = st.form_submit_button("次へ")
        if sub:
            correct = (choice == q["answer"])
            st.session_state.exam_results.append({
                "q": q,
                "choice": choice,
                "correct": correct
            })
            st.session_state.question_index += 1
            st.rerun()

def show_exam_result():
    play_bgm("town")
    results = st.session_state.exam_results
    if not results:
        st.warning("試験データがありません。")
        if st.button("タイトルに戻る"):
            st.session_state.screen = "title"
            st.rerun()
        return

    correct_count = sum(1 for r in results if r["correct"])
    total = len(results)
    rate = (correct_count / total * 100) if total > 0 else 0
    
    st.markdown("## 📊 本試験結果")
    st.markdown(f"**正答数**: {correct_count} / {total} ({rate:.1f}%)")
    
    if rate >= 75:
        st.markdown("<div class='exam-result-pass'>🏆 S 合格確実！余裕の合格ラインです！</div>", unsafe_allow_html=True)
    elif rate >= 65:
        st.markdown("<div class='exam-result-pass'>✅ A 合格圏内！合格ラインを超えています！</div>", unsafe_allow_html=True)
    elif rate >= 60:
        st.markdown("<div class='exam-result-fail'>⚠️ B 合格ギリギリ。苦手分野を復習しよう！</div>", unsafe_allow_html=True)
    elif rate >= 50:
        st.markdown("<div class='exam-result-fail'>❌ C 要復習。苦手分野が足を引っ張っています</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='exam-result-fail'>💀 D 要基礎固め。基礎からやり直しが必要です。</div>", unsafe_allow_html=True)
        
    st.divider()
    st.markdown("### 📝 間違えた問題と解説")
    for i, r in enumerate(results):
        if not r["correct"]:
            q = r["q"]
            with st.expander(f"Q{i+1}: {q['question']}"):
                st.markdown(f"**あなたの解答**: {r['choice']}  |  **正解**: {q['answer']}")
                st.markdown(f"**解説**: {q['explanation']}")
                
    if st.button("タイトルに戻る", type="primary", use_container_width=True):
        st.session_state.screen = "title"
        st.rerun()

def show_weakness_select():
    play_bgm("town")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("## 🎯 弱点特訓道場")
    with col2:
        if st.button("◀ タイトルに戻る"):
            st.session_state.screen = "title"
            st.rerun()
            
    render_status_bar()
    
    wrong_ids = st.session_state.get("wrong_questions", [])
    if not wrong_ids:
        show_nanami_message("すごい！今のところ苦手な問題はないみたいだね！")
        return
        
    wq = [q for q in QUESTIONS if q.get("id") in wrong_ids]
    st.markdown(f"現在、あなたが間違えた問題は **{len(wq)}問** あります。")
    show_nanami_message("間違えた問題に何度も挑戦して、弱点を克服しよう！")
    
    if st.button("⚔️ 弱点の魔物たちに挑む", type="primary", use_container_width=True):
        st.session_state.current_dungeon = "weakness"
        st.session_state.current_domain = "all"
        st.session_state.current_questions = random.sample(wq, min(10, len(wq)))
        st.session_state.question_index = 0
        st.session_state.screen = "battle"
        st.session_state.hp = 100
        st.session_state.combo = 0
        init_battle_state()
        st.rerun()

def show_category_select():
    play_bgm("town")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("## 📚 カテゴリ別修練場")
    with col2:
        if st.button("◀ タイトルに戻る"):
            st.session_state.screen = "title"
            st.rerun()
            
    render_status_bar()
    
    show_nanami_message("特定の分野を集中的に鍛える場所だよ！鍛えたい分野を選んでね。")
    categories = list(set([q["category"] for q in QUESTIONS]))
    
    cols = st.columns(2)
    for i, cat in enumerate(categories):
        with cols[i%2]:
            if st.button(f"📘 {cat} の試練", use_container_width=True):
                cq = [q for q in QUESTIONS if q["category"] == cat]
                st.session_state.current_dungeon = f"category_{cat}"
                st.session_state.current_domain = "all"
                st.session_state.current_questions = random.sample(cq, min(10, len(cq)))
                st.session_state.question_index = 0
                st.session_state.screen = "battle"
                st.session_state.hp = 100
                st.session_state.combo = 0
                init_battle_state()
                st.rerun()
