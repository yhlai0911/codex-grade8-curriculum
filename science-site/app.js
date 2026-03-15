const modules = [
  {
    id: "mass",
    tag: "學習站 1",
    title: "化學反應與質量守恆",
    scene:
      "你在科展準備室中混合兩種藥品，桌上冒出氣泡。老師問你：看到的東西變了，總質量也跟著消失了嗎？",
    mission:
      "學會分辨物理變化與化學變化，並用粒子觀點說明為什麼化學反應前後總質量守恆。",
    coreModel: "原子重新排列，但總原子數不變，所以封閉系統中的總質量守恆。",
    coreDecision: "看到現象改變時，要判斷它是單純狀態改變，還是已經生成新物質。",
    badge: "質量守門員",
    cliffhanger: "下一站你會看到：有些反應不只生成新物質，還伴隨電子轉移，這就是氧化還原的入口。",
    goals: [
      "用顏色、氣味、沉澱、放熱等現象判斷是否發生化學變化。",
      "說出質量守恆的前提是封閉系統，而不是任何情況都直接量得一樣。",
      "能用『反應前後原子只是重新排列』解釋守恆。",
      "能完成簡單質量計算。"
    ],
    prerequisites: ["知道物質由粒子組成。", "能區分質量與體積不是同一件事。", "理解實驗容器開口與密閉會影響量測結果。"],
    checkpoint: {
      title: "看到氣體逃走時，先問自己兩件事",
      points: ["系統是不是開放的？", "如果把逃走的氣體也算進去，總質量有沒有改變？"]
    },
    theory: [
      {
        title: "直覺問題",
        body: "木柴燃燒後剩下的灰很少，為什麼不能直接說『質量變少了，所以不守恆』？因為有一部分物質已經變成看不見的氣體跑到空氣中。"
      },
      {
        title: "定義",
        body: "化學反應是舊物質中的原子重新組合，生成具有新性質的新物質。反應中原子的種類與數目不會憑空增減。"
      },
      {
        title: "模型",
        body: "封閉系統中：反應物總質量 = 生成物總質量。你看到的只是組合方式改變，不是原子消失。"
      },
      {
        title: "管理意義",
        body: "做實驗或解題時，先決定『哪些東西要列入系統』。如果系統界線畫錯，後面的判斷很容易整題失準。"
      }
    ],
    example: {
      title: "碳酸氫鈉與醋酸反應",
      steps: [
        "密閉袋中放入 10 g 小蘇打與 40 g 醋。",
        "反應產生二氧化碳，但因為袋子密封，氣體沒有逸散。",
        "反應前總質量 = 10 + 40 = 50 g。",
        "反應後袋中液體、殘餘固體與氣體全部仍在袋內。",
        "因此反應後總質量仍為 50 g。"
      ],
      answer: "關鍵不是『有沒有冒泡』，而是『生成的氣體有沒有被算進系統』。"
    },
    pbl: {
      title: "怎麼設計不會誤判的實驗？",
      scenario:
        "你要向同學證明質量守恆，下列四種做法只能選一種，哪一個最能避免爭議？",
      options: [
        {
          title: "A. 開口燒杯混合後直接秤",
          desc: "冒出的氣體會離開系統，質量數字容易變小。",
          good: false
        },
        {
          title: "B. 用密封袋裝反應物再混合",
          desc: "氣體被保留在袋內，最能完整量到系統總質量。",
          good: true
        },
        {
          title: "C. 只量固體殘渣",
          desc: "忽略液體與氣體，資訊明顯不足。",
          good: false
        },
        {
          title: "D. 靠肉眼看體積有沒有變",
          desc: "體積改變不等於質量改變。",
          good: false
        }
      ],
      reasoning: [
        "先想要證明的是質量守恆，不是體積守恆。",
        "再檢查反應中是否會產生氣體。",
        "如果有氣體，就要選能把氣體留下來的密閉系統。",
        "因此 B 最合理。"
      ]
    },
    myths: [
      {
        title: "迷思 1：看到沉澱或冒泡才算化學反應",
        text: "有些化學反應的現象很不明顯，但只要生成新物質，仍然是化學變化。"
      },
      {
        title: "迷思 2：秤到數字變小就代表不守恆",
        text: "很多時候只是漏算逃出的氣體，並不是原子真的消失。"
      }
    ],
    boss: {
      prompt:
        "班上同學說：『蠟燭燒完只剩一點灰，所以質量明顯變少，不符合質量守恆。』請用不超過 80 字反駁他。",
      checklist: ["點出有氣體生成並進入空氣。", "說明若把所有生成物都算入，總質量仍守恆。"]
    },
    flashcards: [
      { front: "什麼情況最適合驗證質量守恆？", back: "反應必須在封閉系統中進行，才能把氣體也算進去。" },
      { front: "化學反應的微觀本質是什麼？", back: "原子重新排列，種類與總數不變。" },
      { front: "體積變化能直接判斷質量是否守恆嗎？", back: "不能。體積與質量是不同物理量。" }
    ],
    cram: {
      mustKnow: [
        "質量守恆一定先看系統是否封閉，尤其是有氣體生成時。",
        "判斷化學變化要抓『生成新物質』，不是只看外觀大小改變。",
        "微觀理由要背：原子重新排列，總原子數不變。"
      ],
      traps: [
        "把『秤到的數值變小』直接當成不守恆，忽略氣體逸散。",
        "把體積改變誤當質量改變。",
        "把融化、蒸發、溶解都誤判成化學變化。"
      ],
      memoryHook: "守恆先看界線，變化先看有沒有新物質；氣體跑掉不是原子消失。",
      finalDrill: "開口燒杯中的鎂與酸反應後質量變小，請用 2 句話解釋為什麼不能據此否定質量守恆。"
    },
    quiz: [
      {
        question: "下列何者最能直接作為化學變化的證據？",
        choices: ["冰塊融化成水", "砂糖溶於水", "生成沉澱或新氣體", "鐵絲被拉長"],
        answer: 2,
        explanation: "生成沉澱或氣體通常代表出現新物質。"
      },
      {
        question: "某反應在開口燒杯中進行後質量變小，最合理的解釋是什麼？",
        choices: ["原子數變少", "氣體逸散未被計入", "質量守恆只適用固體", "反應物不夠純"],
        answer: 1,
        explanation: "開放系統常因氣體逸散而造成量測值變小。"
      },
      {
        question: "質量守恆的微觀原因是什麼？",
        choices: ["粒子體積不變", "原子總數不變", "物質顏色不變", "反應速率固定"],
        answer: 1,
        explanation: "化學反應中原子只是重新排列，總數不變。"
      }
    ],
    lab: { type: "mass" }
  },
  {
    id: "redox",
    tag: "學習站 2",
    title: "氧化還原與生活中的化學",
    scene:
      "校園腳踏車停車棚裡，一台車才放一學期就生鏽，另一台卻幾乎沒事。到底是誰偷走了金屬的亮面？",
    mission:
      "掌握氧化與還原的對應關係，並用生活例子理解燃燒、生鏽、漂白與金屬提煉。",
    coreModel: "氧化是得氧、失氫或失電子；還原則是失氧、得氫或得電子。",
    coreDecision: "觀察反應時，要判斷哪個物質被氧化、哪個物質被還原，以及環境如何影響反應快慢。",
    badge: "電子追蹤員",
    cliffhanger: "再往下，你會發現溶液中的離子能讓電流通過，化學反應和導電性會正式接軌。",
    goals: [
      "能用國中常見定義說出氧化與還原。",
      "能辨識燃燒、生鏽、金屬冶煉中的氧化還原角色。",
      "理解水、氧氣、鹽分會影響生鏽速度。",
      "能用生活判斷避免金屬腐蝕。"
    ],
    prerequisites: ["知道氧氣常參與燃燒與腐蝕。", "知道金屬表面會和環境接觸。", "能讀懂簡單條件比較。"],
    checkpoint: {
      title: "判斷氧化還原時的快速提問",
      points: ["誰得到氧？", "誰失去氧？", "環境有沒有讓反應更容易進行？"]
    },
    theory: [
      {
        title: "直覺問題",
        body: "鐵釘放著放著變紅褐色，外表看起來像『髒掉』，其實它已經和氧反應，生成新的氧化鐵。"
      },
      {
        title: "定義",
        body: "在國中常見表述中，物質得到氧叫氧化；失去氧叫還原。氧化和還原通常成對出現。"
      },
      {
        title: "範例",
        body: "氧化銅遇到氫氣可被還原成銅；氫氣同時被氧化成水。你不能只看一邊，要看整體。"
      },
      {
        title: "生活意義",
        body: "防鏽漆、鍍鋅、保持乾燥，本質上都是在降低金屬接觸氧與水的機會，或讓別的金屬先被氧化。"
      }
    ],
    example: {
      title: "比較三支鐵釘的生鏽速度",
      steps: [
        "甲：只有乾燥空氣；乙：有水與空氣；丙：有鹽水與空氣。",
        "甲缺少水，生鏽最慢。",
        "乙同時有水與氧氣，會生鏽。",
        "丙除了水與氧氣，還有鹽分讓腐蝕更快。",
        "因此速度：丙 > 乙 > 甲。"
      ],
      answer: "水與氧是生鏽基本條件，鹽分會進一步加速。"
    },
    pbl: {
      title: "海邊腳踏車該怎麼保養？",
      scenario:
        "你住在海邊，腳踏車常被鹹濕空氣影響。要選一種最有效的優先做法。",
      options: [
        {
          title: "A. 用濕布長時間覆蓋金屬",
          desc: "增加水分接觸，會更糟。",
          good: false
        },
        {
          title: "B. 定期擦乾並補上防鏽層",
          desc: "降低水氧接觸，切斷腐蝕條件。",
          good: true
        },
        {
          title: "C. 放在戶外曬鹽霧",
          desc: "鹽分會加快腐蝕。",
          good: false
        },
        {
          title: "D. 只看顏色變化再處理",
          desc: "等鏽明顯出現時往往已經受損。",
          good: false
        }
      ],
      reasoning: [
        "先找出生鏽條件：水、氧、鹽分。",
        "海邊最麻煩的是濕氣與鹽霧。",
        "有效策略是降低接觸，不是等反應發生後再看。",
        "因此 B 最合理。"
      ]
    },
    myths: [
      {
        title: "迷思 1：只有接觸到火才叫氧化",
        text: "燃燒是快速氧化，生鏽則是慢速氧化，兩者都屬於氧化。"
      },
      {
        title: "迷思 2：金屬越硬越不會生鏽",
        text: "是否生鏽主要看材質與環境條件，不是看硬不硬。"
      }
    ],
    boss: {
      prompt:
        "如果要設計一個『三天內看出差異』的生鏽實驗，你會控制哪些條件、比較哪三組？",
      checklist: ["至少提到水、氧與鹽分。", "說明哪個條件固定、哪個條件改變。"]
    },
    flashcards: [
      { front: "生鏽是快速還是慢速氧化？", back: "慢速氧化。" },
      { front: "鐵釘要生鏽，最基本需要哪兩項？", back: "水與氧氣。" },
      { front: "鍍鋅為什麼能防鏽？", back: "鋅較容易先被氧化，保護內層鐵。" }
    ],
    cram: {
      mustKnow: [
        "燃燒和生鏽都屬氧化，只是反應速率不同。",
        "鐵生鏽至少要有水與氧，鹽分會進一步加快。",
        "國中題常用『得氧是氧化、失氧是還原』來判斷。"
      ],
      traps: [
        "只背『有火才叫氧化』，忽略慢速氧化。",
        "把海邊生鏽快只歸因於太陽，不提水與鹽分。",
        "看氧化還原只看一邊，忘記另一邊會同時發生相反變化。"
      ],
      memoryHook: "得氧叫氧化，失氧叫還原；水氧是基本，鹽分會催快。",
      finalDrill: "比較乾燥空氣、清水、鹽水三種環境中的鐵釘，寫出生鏽速度排序並說理由。"
    },
    quiz: [
      {
        question: "下列何者最能加快鐵生鏽？",
        choices: ["乾燥空氣", "鹽水與空氣", "真空環境", "完全油封隔絕"],
        answer: 1,
        explanation: "鹽水與空氣提供水、氧與電解質環境，最易生鏽。"
      },
      {
        question: "燃燒與生鏽的共同點是什麼？",
        choices: ["都屬於氧化反應", "都需要酸鹼中和", "都一定產生沉澱", "都不能逆轉"],
        answer: 0,
        explanation: "兩者都屬於氧化，只是速率不同。"
      },
      {
        question: "若某物質失去氧，依國中定義可說它發生了什麼？",
        choices: ["氧化", "還原", "蒸發", "中和"],
        answer: 1,
        explanation: "失去氧就是還原。"
      }
    ],
    lab: { type: "rust" }
  },
  {
    id: "electrolyte",
    tag: "學習站 3",
    title: "電解質、酸鹼與 pH",
    scene:
      "同樣是透明液體，鹽水可以讓小燈泡亮起來，糖水卻幾乎沒反應。差別藏在哪裡？",
    mission:
      "理解電解質與非電解質的差異，認識酸鹼在水中的表現，並能讀懂 pH 數值。",
    coreModel: "溶液是否能導電，取決於其中是否有可自由移動的離子。",
    coreDecision: "看到一瓶溶液時，要判斷它是否含離子、是酸性還是鹼性，以及 pH 大致落在哪一區。",
    badge: "離子導航員",
    cliffhanger: "最後一站，你會把酸與鹼放在一起，看看中和後怎麼形成鹽和水。",
    goals: [
      "能區分電解質與非電解質。",
      "知道酸性溶液含較多 H+，鹼性溶液含較多 OH-。",
      "能用 pH 判斷酸鹼強弱方向。",
      "會解讀常見指示劑的顏色改變。"
    ],
    prerequisites: ["知道溶液是溶質分散在溶劑中。", "理解導電需要帶電粒子移動。", "會比較數值大小。"],
    checkpoint: {
      title: "判讀 pH 的兩條快速規則",
      points: ["pH < 7 為酸性，pH = 7 為中性，pH > 7 為鹼性。", "pH 越小不代表『越危險』，而是代表酸性越強。"]
    },
    theory: [
      {
        title: "直覺問題",
        body: "同樣放在水裡，食鹽能變成帶電粒子，糖卻多半以中性分子存在，所以導電性差很多。"
      },
      {
        title: "定義",
        body: "電解質是溶於水後可形成離子的物質；非電解質溶於水後大多不產生離子。"
      },
      {
        title: "酸鹼模型",
        body: "國中常用觀點是：酸性溶液含較多 H+，鹼性溶液含較多 OH-，pH 用來描述酸鹼程度。"
      },
      {
        title: "生活意義",
        body: "清潔劑、醋、汽水、肥皂水都有酸鹼差異。會讀 pH，才能安全使用並判斷是否需要稀釋。"
      }
    ],
    example: {
      title: "判讀四種溶液的導電與酸鹼",
      steps: [
        "甲為食鹽水，乙為糖水，丙為檸檬汁，丁為肥皂水。",
        "食鹽水可形成離子，屬電解質，接近中性或微偏鹼。",
        "糖水幾乎不形成離子，屬非電解質，通常接近中性。",
        "檸檬汁屬酸性，pH 小於 7；肥皂水屬鹼性，pH 大於 7。"
      ],
      answer: "導電性與酸鹼性是不同判斷軸，但都和溶液中粒子狀態有關。"
    },
    pbl: {
      title: "露營時該怎麼判斷液體用途？",
      scenario:
        "桌上有三瓶無標籤液體：糖水、鹽水、稀釋白醋。你手上只有導電裝置與 pH 試紙，該怎麼分辨？",
      options: [
        {
          title: "A. 只看顏色深淺",
          desc: "透明液體外觀太像，資訊不足。",
          good: false
        },
        {
          title: "B. 先測導電，再測 pH",
          desc: "可先排除糖水，再用 pH 區分鹽水與白醋。",
          good: true
        },
        {
          title: "C. 直接聞味道決定",
          desc: "不安全，也可能誤判。",
          good: false
        },
        {
          title: "D. 全部加熱看誰先蒸發",
          desc: "蒸發速率無法可靠區分三者。",
          good: false
        }
      ],
      reasoning: [
        "糖水幾乎不導電，可先被辨認出來。",
        "剩下鹽水與白醋都可導電，但白醋呈酸性。",
        "再用 pH 試紙就能做最後區分。",
        "所以 B 是最有效率的流程。"
      ]
    },
    myths: [
      {
        title: "迷思 1：能導電就一定是酸",
        text: "鹽水、鹼性溶液也能導電，因為關鍵是有離子，不是只有酸。"
      },
      {
        title: "迷思 2：pH 6 和 pH 5 只差一點點",
        text: "pH 是刻度，雖然國中多做方向判讀，但不能把它當成線性感覺量。"
      }
    ],
    boss: {
      prompt:
        "請設計一張『導電性 x pH』二維表，把糖水、鹽水、汽水、肥皂水放進正確位置。",
      checklist: ["至少有能不能導電一軸。", "至少有酸、中、鹼一軸。"]
    },
    flashcards: [
      { front: "什麼是電解質？", back: "溶於水後可產生離子，因此能導電的物質。" },
      { front: "pH 大於 7 代表什麼？", back: "代表溶液呈鹼性。" },
      { front: "糖水為什麼不易導電？", back: "因為糖溶於水後大多不形成離子。" }
    ],
    cram: {
      mustKnow: [
        "能不能導電，關鍵是溶液中有沒有自由移動的離子。",
        "pH 小於 7 酸性，大於 7 鹼性，等於 7 中性。",
        "糖水通常不導電；鹽水、酸、鹼溶液通常可導電。"
      ],
      traps: [
        "把『能導電』直接等同『一定是酸』。",
        "把 pH 當成危險程度排行，而不是酸鹼程度指標。",
        "只記顏色變化，忘了先判斷酸中鹼。"
      ],
      memoryHook: "先看有沒有離子，再看 pH 落哪邊；導電性和酸鹼性要分開判。",
      finalDrill: "你有糖水、鹽水、白醋三瓶透明液體，只有導電器和 pH 試紙時，請寫出最省步驟的辨認順序。"
    },
    quiz: [
      {
        question: "下列哪一種水溶液最不容易導電？",
        choices: ["食鹽水", "稀鹽酸", "糖水", "氫氧化鈉溶液"],
        answer: 2,
        explanation: "糖水屬非電解質，不易形成離子。"
      },
      {
        question: "若某溶液 pH = 3，最合理的判斷是什麼？",
        choices: ["強鹼", "中性", "酸性", "無法判斷"],
        answer: 2,
        explanation: "pH 小於 7 為酸性。"
      },
      {
        question: "導電性的直接關鍵是什麼？",
        choices: ["顏色夠深", "有沒有自由移動的離子", "液體一定要很熱", "分子一定很大"],
        answer: 1,
        explanation: "能否導電取決於是否存在可移動的帶電粒子。"
      }
    ],
    lab: { type: "ph" }
  },
  {
    id: "neutralization",
    tag: "學習站 4",
    title: "酸鹼中和與鹽類應用",
    scene:
      "胃酸過多時，藥師為什麼不是直接叫你喝大量清水，而是選擇含鹼性成分的制酸劑？",
    mission:
      "理解中和反應的本質，知道酸與鹼反應後會形成鹽和水，並能把概念用在生活決策。",
    coreModel: "酸中的 H+ 與鹼中的 OH- 作用生成水；其餘離子組成鹽。",
    coreDecision: "面對過酸或過鹼環境時，要判斷是否適合用中和方式處理，以及用量是否過多。",
    badge: "中和調停者",
    cliffhanger: "你已經完成國二下自然的核心化學地圖，下一步可以進入題組練習或實驗設計。",
    goals: [
      "能說出中和反應的生成物。",
      "知道中和後不一定剛好 pH = 7，仍與用量有關。",
      "能把中和應用到胃藥、土壤改良、廢水處理等情境。",
      "能從『過量』角度判讀實驗結果。"
    ],
    prerequisites: ["知道酸與鹼的基本判讀。", "知道 H+ 與 OH- 的角色。", "理解『剛好反應完』與『過量』不同。"],
    checkpoint: {
      title: "中和題最容易忽略的地方",
      points: ["中和不是一定得到中性。", "要看哪一方剩下來。", "生活應用要兼顧安全與用量。"]
    },
    theory: [
      {
        title: "直覺問題",
        body: "酸加鹼後刺激性可能降低，但如果你加太多鹼，最後得到的溶液仍可能偏鹼，不會自動變成中性。"
      },
      {
        title: "定義",
        body: "中和反應是酸和鹼反應生成鹽與水。微觀上可想成 H+ 和 OH- 結合成水。"
      },
      {
        title: "判讀重點",
        body: "若酸剛好和鹼完全反應，溶液最接近中性；若其中一方過量，溶液就會保留那一方的性質。"
      },
      {
        title: "生活意義",
        body: "制酸劑、酸性土壤改良、工廠廢水處理都在用中和，但都不能亂加，因為過量會造成新的問題。"
      }
    ],
    example: {
      title: "中和到哪裡最剛好？",
      steps: [
        "某酸性溶液需要 20 mL 的鹼液才剛好完全中和。",
        "如果只加 10 mL，酸仍過量，溶液仍偏酸。",
        "如果加到 20 mL，最接近完全中和。",
        "如果加到 30 mL，鹼過量，溶液改為偏鹼。"
      ],
      answer: "中和要看相對用量，不是『有加到鹼』就一定中性。"
    },
    pbl: {
      title: "胃酸過多時該怎麼做？",
      scenario:
        "你要向同學解釋制酸劑的原理，下列哪一種說法最完整？",
      options: [
        {
          title: "A. 因為鹼比較冷，所以能降溫",
          desc: "把中和誤解成溫度效果。",
          good: false
        },
        {
          title: "B. 鹼與胃酸反應，降低過多酸性",
          desc: "說出中和本質，也符合生活應用。",
          good: true
        },
        {
          title: "C. 只要喝越多鹼性飲料越好",
          desc: "忽略過量風險。",
          good: false
        },
        {
          title: "D. 中和後一定完全無任何離子",
          desc: "錯，中和後仍可能有鹽類離子存在。",
          good: false
        }
      ],
      reasoning: [
        "先確認問題是酸性過多。",
        "再找能與酸作用的物質，鹼最符合。",
        "但重點是適量中和，不是無限量補鹼。",
        "因此 B 是最完整的說法。"
      ]
    },
    myths: [
      {
        title: "迷思 1：中和後一定沒有任何味道或性質",
        text: "中和後仍可能留下鹽類，若反應未剛好完成，還可能偏酸或偏鹼。"
      },
      {
        title: "迷思 2：鹼可以無限制中和酸",
        text: "過量鹼本身也可能刺激或危險，所以生活中一定要控制用量。"
      }
    ],
    boss: {
      prompt:
        "設計一句給國一學弟妹的提醒，教他們分辨『有中和』和『剛好中和』的差別。",
      checklist: ["要提到過量概念。", "要提到 pH 不一定剛好等於 7。"]
    },
    flashcards: [
      { front: "中和反應的主要生成物是什麼？", back: "鹽和水。" },
      { front: "酸和鹼反應後一定 pH = 7 嗎？", back: "不一定，要看兩者是否剛好完全反應。" },
      { front: "制酸劑的核心原理是什麼？", back: "用適量鹼性物質中和過多胃酸。" }
    ],
    cram: {
      mustKnow: [
        "中和反應的核心生成物是鹽和水。",
        "中和後不一定剛好中性，要看哪一方過量。",
        "生活應用最常考制酸劑、酸性土壤改良與廢水處理。"
      ],
      traps: [
        "把『有加鹼』誤認成『一定 pH = 7』。",
        "只寫出水，忘記還會生成鹽。",
        "忽略過量概念，無法判讀最後溶液性質。"
      ],
      memoryHook: "酸鹼先看剩誰，剩酸偏酸、剩鹼偏鹼；剛好才最接近中性。",
      finalDrill: "某酸液需 20 mL 鹼液才能完全中和，若只加 12 mL 或加到 30 mL，最後各偏什麼性質？"
    },
    quiz: [
      {
        question: "酸與鹼中和後一定產生什麼？",
        choices: ["氧氣與水", "鹽與水", "糖與水", "只有沉澱"],
        answer: 1,
        explanation: "中和反應的典型生成物是鹽與水。"
      },
      {
        question: "若鹼加入過量，反應後溶液最可能如何？",
        choices: ["仍偏酸", "一定中性", "偏鹼", "完全沒有離子"],
        answer: 2,
        explanation: "鹼過量時，溶液會呈現鹼性。"
      },
      {
        question: "下列哪個生活例子最符合中和應用？",
        choices: ["用肥皂洗手", "用制酸劑緩解胃酸過多", "把糖加入茶中", "冰塊放入果汁"],
        answer: 1,
        explanation: "制酸劑是典型酸鹼中和應用。"
      }
    ],
    lab: { type: "neutral" }
  }
];

const storageKey = "science-site-progress";
const sprintPool = modules.flatMap((module) =>
  module.quiz.map((question, index) => ({
    ...question,
    moduleId: module.id,
    moduleTitle: module.title,
    sourceLabel: `${module.tag}｜${module.title}`,
    id: `${module.id}-sprint-${index}`
  }))
);
const sprintQuestionCount = 6;
const defaultProgress = { completed: {}, bestScores: {}, sprintBest: 0 };
let state = {
  currentModule: 0,
  cardIndex: 0,
  cardFlipped: false,
  guideStep: 0,
  guidedMode: true,
  activeTool: "sprint",
  progress: loadProgress(),
  sprintSet: [],
  lastSprintSummary: []
};
let focusTimerId = null;
let focusSecondsLeft = 180;

const moduleNav = document.getElementById("module-nav");
const completedCount = document.getElementById("completed-count");
const bestScore = document.getElementById("best-score");
const dailyTask = document.getElementById("daily-task");
const cramFocus = document.getElementById("cram-focus");
const startLearning = document.getElementById("start-learning");
const toggleGuidedMode = document.getElementById("toggle-guided-mode");
const resetProgress = document.getElementById("reset-progress");
const jumpToSprint = document.getElementById("jump-to-sprint");
const toggleComplete = document.getElementById("toggle-complete");
const flashcard = document.getElementById("flashcard");
const nextCard = document.getElementById("next-card");
const submitQuiz = document.getElementById("submit-quiz");
const quizForm = document.getElementById("quiz-form");
const quizResult = document.getElementById("quiz-result");
const labContainer = document.getElementById("lab-container");
const mustKnowList = document.getElementById("must-know-list");
const trapList = document.getElementById("trap-list");
const memoryHook = document.getElementById("memory-hook");
const finalDrill = document.getElementById("final-drill");
const weakTopicList = document.getElementById("weak-topic-list");
const planList = document.getElementById("plan-list");
const cramStatus = document.getElementById("cram-status");
const sprintForm = document.getElementById("sprint-form");
const sprintResult = document.getElementById("sprint-result");
const submitSprint = document.getElementById("submit-sprint");
const regenSprint = document.getElementById("regen-sprint");
const focusTimer = document.getElementById("focus-timer");
const guideMessage = document.getElementById("guide-message");
const guideStepTag = document.getElementById("guide-step-tag");
const guideStepTitle = document.getElementById("guide-step-title");
const guideStepDesc = document.getElementById("guide-step-desc");
const guideStepChecklist = document.getElementById("guide-step-checklist");
const guideProgressLabel = document.getElementById("guide-progress-label");
const guideProgressFill = document.getElementById("guide-progress-fill");
const guideAction = document.getElementById("guide-action");
const guideDone = document.getElementById("guide-done");
const guideEasier = document.getElementById("guide-easier");
const toolTabs = document.querySelectorAll("[data-tool]");
const toolPanels = document.querySelectorAll("[data-tool-panel]");

function loadProgress() {
  const raw = localStorage.getItem(storageKey);
  if (!raw) return structuredClone(defaultProgress);
  try {
    const parsed = JSON.parse(raw);
    return {
      completed: { ...defaultProgress.completed, ...(parsed.completed ?? {}) },
      bestScores: { ...defaultProgress.bestScores, ...(parsed.bestScores ?? {}) },
      sprintBest: parsed.sprintBest ?? 0
    };
  } catch {
    return structuredClone(defaultProgress);
  }
}

function saveProgress() {
  localStorage.setItem(storageKey, JSON.stringify(state.progress));
  renderSummary();
  renderNav();
}

function getModuleMastery(moduleId) {
  return state.progress.bestScores[moduleId] ?? 0;
}

function getWeakModules() {
  return [...modules].sort((a, b) => getModuleMastery(a.id) - getModuleMastery(b.id));
}

function getGuideTasks(module) {
  const mastery = getModuleMastery(module.id);
  return [
    {
      tag: "第 1 步 / 30 秒",
      title: "先看這章 3 個必考點",
      desc: "現在不要讀完整章，只看上面的補強區就夠。",
      checklist: ["看完 3 個高頻必考點。", "把 30 秒口訣唸一次。"],
      targetId: "cram-overview-panel",
      buttonLabel: "看必考點"
    },
    {
      tag: "第 2 步 / 1 分鐘",
      title: "翻 1 張卡，讓腦袋開機",
      desc: "答對答錯都沒關係，先讓自己進入作答狀態。",
      checklist: ["按右邊抽認卡。", "自己說出答案一次。"],
      targetId: "flashcard-panel",
      buttonLabel: "翻卡片"
    },
    mastery < 70
      ? {
          tag: "第 3 步 / 2 分鐘",
          title: "只答本章第一題",
          desc: "不用整份寫完。先答第一題，再看解析就好。",
          checklist: ["先答第一題。", "按批改，看自己錯在哪。"],
          targetId: "quiz-panel",
          buttonLabel: "去答 1 題"
        }
      : {
          tag: "第 3 步 / 3 分鐘",
          title: "做一回混合快測",
          desc: "如果本章有底子，就直接用快測找最弱單元。",
          checklist: ["先做快測前 3 題。", "批改後只看最弱單元。"],
          targetId: "sprint-panel",
          buttonLabel: "做快測"
        }
  ];
}

function buildCramPlan() {
  const formatter = new Intl.DateTimeFormat("zh-TW", { month: "numeric", day: "numeric" });
  const planTemplates = [
    "質量守恆與化學變化快判",
    "氧化還原、生鏽條件與防鏽",
    "電解質、導電性與 pH",
    "酸鹼中和、過量與生活應用",
    "四章混合錯題重做",
    "段考衝刺快測 2 回",
    "只看口訣、陷阱與 Boss 任務"
  ];

  return planTemplates.map((task, index) => {
    const date = new Date();
    date.setDate(date.getDate() + index);
    return `${formatter.format(date)}：${task}`;
  });
}

function renderFocusTimer() {
  const minutes = String(Math.floor(focusSecondsLeft / 60)).padStart(1, "0");
  const seconds = String(focusSecondsLeft % 60).padStart(2, "0");
  focusTimer.textContent = `${minutes}:${seconds}`;
}

function stopFocusTimer() {
  if (focusTimerId) {
    window.clearInterval(focusTimerId);
    focusTimerId = null;
  }
  focusSecondsLeft = 180;
  renderFocusTimer();
}

function startFocusTimer() {
  stopFocusTimer();
  focusTimerId = window.setInterval(() => {
    focusSecondsLeft -= 1;
    renderFocusTimer();
    if (focusSecondsLeft <= 0) {
      window.clearInterval(focusTimerId);
      focusTimerId = null;
      guideMessage.textContent = "3 分鐘到了。現在不要加量，直接按「我做完了，下一步」或先去批改。";
    }
  }, 1000);
}

function focusTarget(targetId) {
  const toolMap = {
    "sprint-panel": "sprint",
    "quiz-panel": "quiz",
    "flashcard-panel": "flashcard",
    "lab-panel": "lab"
  };
  if (toolMap[targetId]) {
    setActiveTool(toolMap[targetId]);
  }
  const target = document.getElementById(targetId);
  if (!target) return;
  target.scrollIntoView({ behavior: "smooth", block: "start" });
  target.classList.add("spotlight");
  window.setTimeout(() => target.classList.remove("spotlight"), 2200);
}

function renderGuidedMode() {
  document.body.classList.toggle("guided-mode", state.guidedMode);
  toggleGuidedMode.textContent = state.guidedMode ? "切換成完整模式" : "回到專注模式";
}

function renderActiveTool() {
  toolTabs.forEach((tab) => {
    const isActive = tab.dataset.tool === state.activeTool;
    tab.classList.toggle("active", isActive);
    tab.setAttribute("aria-selected", String(isActive));
  });

  toolPanels.forEach((panel) => {
    panel.classList.toggle("active", panel.dataset.toolPanel === state.activeTool);
  });
}

function setActiveTool(toolName) {
  state.activeTool = toolName;
  renderActiveTool();
}

function renderGuide() {
  const module = modules[state.currentModule];
  const tasks = getGuideTasks(module);
  const safeIndex = Math.min(state.guideStep, tasks.length - 1);
  const currentTask = tasks[safeIndex];
  const progress = ((safeIndex + 1) / tasks.length) * 100;
  const weakest = getWeakModules()[0];
  guideMessage.textContent =
    safeIndex === 0
      ? `你現在不用拚完整章。先把 ${module.title} 的最短一步做完。`
      : `做完這一步就好。真的卡住時，先補 ${weakest.title} 也可以。`;
  guideStepTag.textContent = currentTask.tag;
  guideStepTitle.textContent = currentTask.title;
  guideStepDesc.textContent = currentTask.desc;
  guideAction.textContent = currentTask.buttonLabel;
  guideDone.textContent = safeIndex >= tasks.length - 1 ? "這輪做完，重新開始" : "我做完了，下一步";
  guideProgressLabel.textContent = `今日偷吃步進度：${safeIndex + 1} / ${tasks.length}`;
  guideProgressFill.style.width = `${progress}%`;
  renderList("guide-step-checklist", currentTask.checklist);
  renderFocusTimer();
}

function renderCramSidebar() {
  const weakModules = getWeakModules();
  const weakestNames = weakModules.slice(0, 2).map((item) => item.title);
  cramFocus.textContent = weakestNames.length ? `先補：${weakestNames.join("、")}` : "先做混合快測";
  cramStatus.textContent = `建議順序：快測找弱點 -> 回章節補觀念 -> 再做一次混合快測。混合快測最佳 ${state.progress.sprintBest}%`;
  weakTopicList.innerHTML = "";

  if (state.lastSprintSummary.length > 0) {
    state.lastSprintSummary.forEach((item) => {
      const li = document.createElement("li");
      li.textContent = `最新快測弱點：${item}`;
      weakTopicList.appendChild(li);
    });
  } else {
    weakModules.slice(0, 3).forEach((item) => {
      const li = document.createElement("li");
      li.textContent = `${item.title}｜目前最佳 ${getModuleMastery(item.id)}%`;
      weakTopicList.appendChild(li);
    });
  }

  planList.innerHTML = "";
  buildCramPlan().forEach((entry) => {
    const li = document.createElement("li");
    li.textContent = entry;
    planList.appendChild(li);
  });
}

function renderSummary() {
  const completed = Object.values(state.progress.completed).filter(Boolean).length;
  const scores = Object.values(state.progress.bestScores);
  const avg = scores.length
    ? Math.round(scores.reduce((sum, value) => sum + value, 0) / scores.length)
    : 0;
  completedCount.textContent = `${completed} / ${modules.length}`;
  bestScore.textContent = `${avg}%`;

  if (completed === 0) {
    dailyTask.textContent = "先完成第一個學習站";
  } else if (completed < modules.length) {
    dailyTask.textContent = `下一站：${modules.find((item) => !state.progress.completed[item.id]).title}`;
  } else {
    dailyTask.textContent = "四站全破，改做 Boss 任務複習";
  }

  renderCramSidebar();
}

function renderNav() {
  moduleNav.innerHTML = "";
  modules.forEach((module, index) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = `module-btn ${index === state.currentModule ? "active" : ""}`;
    const done = state.progress.completed[module.id] ? "已完成" : "未完成";
    const score = state.progress.bestScores[module.id] ?? 0;
    button.innerHTML = `<strong>${module.tag}｜${module.title}</strong><span>${done} · 最佳 ${score}%</span>`;
    button.addEventListener("click", () => {
      state.currentModule = index;
      state.cardIndex = 0;
      state.cardFlipped = false;
      state.guideStep = 0;
      stopFocusTimer();
      renderModule();
    });
    moduleNav.appendChild(button);
  });
}

function renderModule() {
  const module = modules[state.currentModule];
  setText("module-tag", module.tag);
  setText("module-title", module.title);
  setText("module-scene", module.scene);
  setText("module-mission", module.mission);
  setText("module-core-model", module.coreModel);
  setText("module-core-decision", module.coreDecision);
  setText("module-badge", module.badge);
  setText("module-cliffhanger", `下一章預告：${module.cliffhanger}`);
  setText("checkpoint-title", module.checkpoint.title);
  setText("example-title", module.example.title);
  setText("example-answer", module.example.answer);
  setText("pbl-title", module.pbl.title);
  setText("pbl-scenario", module.pbl.scenario);
  setText("boss-prompt", module.boss.prompt);
  setText("memory-hook", module.cram.memoryHook);
  setText("final-drill", module.cram.finalDrill);
  toggleComplete.textContent = state.progress.completed[module.id] ? "已完成本章" : "標記本章完成";

  renderList("module-goals", module.goals);
  renderList("prerequisites", module.prerequisites);
  renderList("checkpoint-points", module.checkpoint.points);
  renderList("example-steps", module.example.steps, true);
  renderList("pbl-reasoning", module.pbl.reasoning, true);
  renderList("boss-checklist", module.boss.checklist);
  renderList("must-know-list", module.cram.mustKnow);
  renderList("trap-list", module.cram.traps);
  renderTheory(module.theory);
  renderOptions(module.pbl.options);
  renderMyths(module.myths);
  renderFlashcard();
  renderQuiz();
  renderLab();
  renderNav();
  renderSummary();
  renderGuide();
  renderGuidedMode();
  renderActiveTool();
}

function renderList(id, items, numbered = false) {
  const target = document.getElementById(id);
  target.innerHTML = "";
  items.forEach((item) => {
    const li = document.createElement("li");
    li.textContent = item;
    target.appendChild(li);
  });
  target.className = numbered ? "step-list" : target.className;
}

function renderTheory(theoryItems) {
  const container = document.getElementById("theory-stack");
  container.innerHTML = "";
  theoryItems.forEach((item) => {
    const card = document.createElement("article");
    card.className = "theory-card";
    card.innerHTML = `<h4>${item.title}</h4><p>${item.body}</p>`;
    container.appendChild(card);
  });
}

function renderOptions(options) {
  const container = document.getElementById("pbl-options");
  container.innerHTML = "";
  options.forEach((option) => {
    const card = document.createElement("article");
    card.className = `option-card ${option.good ? "good" : ""}`;
    card.innerHTML = `<h4>${option.title}</h4><p>${option.desc}</p>`;
    container.appendChild(card);
  });
}

function renderMyths(items) {
  const container = document.getElementById("myth-list");
  container.innerHTML = "";
  items.forEach((item) => {
    const card = document.createElement("article");
    card.className = "myth-item";
    card.innerHTML = `<strong>${item.title}</strong><p>${item.text}</p>`;
    container.appendChild(card);
  });
}

function renderFlashcard() {
  const module = modules[state.currentModule];
  const card = module.flashcards[state.cardIndex % module.flashcards.length];
  const side = state.cardFlipped
    ? { label: "答案", text: card.back }
    : { label: "問題", text: card.front };
  flashcard.innerHTML = `<small>${side.label}</small><strong>${side.text}</strong>`;
}

function renderQuiz() {
  const module = modules[state.currentModule];
  quizForm.innerHTML = "";
  quizResult.innerHTML = "";
  module.quiz.forEach((item, index) => {
    const block = document.createElement("fieldset");
    block.className = "question-card";
    const name = `question-${index}`;
    block.innerHTML = `<legend>${index + 1}. ${item.question}</legend>`;
    const choiceList = document.createElement("div");
    choiceList.className = "choice-list";

    item.choices.forEach((choice, choiceIndex) => {
      const label = document.createElement("label");
      label.className = "choice-item";
      const choiceId = `${module.id}-${name}-${choiceIndex}`;
      label.setAttribute("for", choiceId);
      label.innerHTML = `<input id="${choiceId}" type="radio" name="${name}" value="${choiceIndex}" /><span>${choice}</span>`;
      choiceList.appendChild(label);
    });

    block.appendChild(choiceList);
    quizForm.appendChild(block);
  });
}

function shuffle(items) {
  const copy = [...items];
  for (let index = copy.length - 1; index > 0; index -= 1) {
    const randomIndex = Math.floor(Math.random() * (index + 1));
    [copy[index], copy[randomIndex]] = [copy[randomIndex], copy[index]];
  }
  return copy;
}

function buildSprintSet() {
  const weakIds = getWeakModules()
    .slice(0, 2)
    .map((item) => item.id);
  const preferred = shuffle(sprintPool.filter((item) => weakIds.includes(item.moduleId)));
  const fallback = shuffle(sprintPool.filter((item) => !weakIds.includes(item.moduleId)));
  const selected = [];

  for (const question of [...preferred, ...fallback]) {
    if (selected.some((item) => item.id === question.id)) continue;
    selected.push(question);
    if (selected.length === sprintQuestionCount) break;
  }

  state.sprintSet = shuffle(selected);
}

function renderSprintQuiz() {
  if (state.sprintSet.length === 0) buildSprintSet();
  sprintForm.innerHTML = "";
  sprintResult.innerHTML = "";

  state.sprintSet.forEach((item, index) => {
    const block = document.createElement("fieldset");
    block.className = "question-card";
    const name = `sprint-question-${index}`;
    block.innerHTML = `<legend>${index + 1}. ${item.question}</legend>`;

    const source = document.createElement("p");
    source.className = "subpanel-label";
    source.textContent = item.sourceLabel;
    block.appendChild(source);

    const choiceList = document.createElement("div");
    choiceList.className = "choice-list";

    item.choices.forEach((choice, choiceIndex) => {
      const label = document.createElement("label");
      label.className = "choice-item";
      const choiceId = `${item.id}-${choiceIndex}`;
      label.setAttribute("for", choiceId);
      label.innerHTML = `<input id="${choiceId}" type="radio" name="${name}" value="${choiceIndex}" /><span>${choice}</span>`;
      choiceList.appendChild(label);
    });

    block.appendChild(choiceList);
    sprintForm.appendChild(block);
  });
}

function renderLab() {
  const module = modules[state.currentModule];
  if (module.lab.type === "mass") renderMassLab();
  if (module.lab.type === "rust") renderRustLab();
  if (module.lab.type === "ph") renderPhLab();
  if (module.lab.type === "neutral") renderNeutralLab();
}

function renderMassLab() {
  labContainer.innerHTML = `
    <div class="lab-box">
      <p>拖動下方數值，看看在開放與封閉系統下，量到的反應後質量會怎麼變。</p>
      <div class="lab-controls">
        <label>
          反應物 A 質量（g）
          <div class="slider-row">
            <span>0</span>
            <input id="mass-a" type="range" min="5" max="40" value="12" />
            <span id="mass-a-value">12</span>
          </div>
        </label>
        <label>
          反應物 B 質量（g）
          <div class="slider-row">
            <span>0</span>
            <input id="mass-b" type="range" min="10" max="60" value="28" />
            <span id="mass-b-value">28</span>
          </div>
        </label>
        <div class="switch-row">
          <label class="pill-toggle"><input id="mass-closed" type="checkbox" checked /> 封閉系統</label>
        </div>
      </div>
      <div class="lab-output" id="mass-output"></div>
    </div>
  `;
  ["mass-a", "mass-b", "mass-closed"].forEach((id) => {
    document.getElementById(id).addEventListener("input", updateMassLab);
  });
  updateMassLab();
}

function updateMassLab() {
  const a = Number(document.getElementById("mass-a").value);
  const b = Number(document.getElementById("mass-b").value);
  const closed = document.getElementById("mass-closed").checked;
  const total = a + b;
  const escapedGas = Math.round(total * 0.18);
  const after = closed ? total : total - escapedGas;
  setText("mass-a-value", a);
  setText("mass-b-value", b);
  document.getElementById("mass-output").innerHTML = `
    <strong>模擬結果</strong>
    反應前總質量：${total} g<br />
    反應後量到的質量：${after} g<br />
    ${closed ? "因為系統封閉，氣體也留在裡面，所以量到的總質量不變。" : `因為系統開放，約有 ${escapedGas} g 的氣體逃出容器，所以量到的數值變小。`}
  `;
}

function renderRustLab() {
  labContainer.innerHTML = `
    <div class="lab-box">
      <p>切換環境條件，預測鐵生鏽會有多快。</p>
      <div class="lab-controls">
        <div class="switch-row">
          <label class="pill-toggle"><input id="rust-water" type="checkbox" checked /> 有水分</label>
          <label class="pill-toggle"><input id="rust-oxygen" type="checkbox" checked /> 有氧氣</label>
          <label class="pill-toggle"><input id="rust-salt" type="checkbox" /> 有鹽分</label>
        </div>
      </div>
      <div class="lab-output" id="rust-output"></div>
    </div>
  `;
  ["rust-water", "rust-oxygen", "rust-salt"].forEach((id) => {
    document.getElementById(id).addEventListener("input", updateRustLab);
  });
  updateRustLab();
}

function updateRustLab() {
  const hasWater = document.getElementById("rust-water").checked;
  const hasOxygen = document.getElementById("rust-oxygen").checked;
  const hasSalt = document.getElementById("rust-salt").checked;
  let level = "幾乎不生鏽";
  let reason = "缺少必要條件，氧化難以進行。";

  if (hasWater && hasOxygen) {
    level = hasSalt ? "快速生鏽" : "中速生鏽";
    reason = hasSalt
      ? "水、氧與鹽分同時存在，腐蝕明顯加快。"
      : "具備水與氧氣，已可發生生鏽。";
  } else if (hasWater || hasOxygen) {
    level = "很慢";
    reason = "只具備部分條件，生鏽不明顯。";
  }

  document.getElementById("rust-output").innerHTML = `
    <strong>模擬結果：${level}</strong>
    ${reason}
  `;
}

function renderPhLab() {
  labContainer.innerHTML = `
    <div class="lab-box">
      <p>拖動 pH 刻度，看看溶液會落在哪個區間，以及常見指示劑可能呈現的顏色。</p>
      <div class="lab-controls">
        <label>
          pH 值
          <div class="slider-row">
            <span>0</span>
            <input id="ph-value" type="range" min="0" max="14" value="7" />
            <span id="ph-value-label">7</span>
          </div>
        </label>
      </div>
      <div class="lab-output" id="ph-output"></div>
    </div>
  `;
  document.getElementById("ph-value").addEventListener("input", updatePhLab);
  updatePhLab();
}

function updatePhLab() {
  const value = Number(document.getElementById("ph-value").value);
  setText("ph-value-label", value);
  let type = "中性";
  let color = "石蕊接近紫色";
  let example = "純水";

  if (value < 7) {
    type = "酸性";
    color = "藍色石蕊偏紅";
    example = value <= 3 ? "像檸檬汁或較酸的飲料" : "像微酸溶液";
  } else if (value > 7) {
    type = "鹼性";
    color = "紅色石蕊偏藍";
    example = value >= 11 ? "像清潔用鹼性溶液" : "像肥皂水";
  }

  document.getElementById("ph-output").innerHTML = `
    <strong>模擬結果：${type}</strong>
    指示劑判讀：${color}<br />
    生活聯想：${example}
  `;
}

function renderNeutralLab() {
  labContainer.innerHTML = `
    <div class="lab-box">
      <p>調整酸與鹼的量，觀察反應後是偏酸、接近中性還是偏鹼。</p>
      <div class="lab-controls">
        <label>
          酸的量
          <div class="slider-row">
            <span>0</span>
            <input id="neutral-acid" type="range" min="0" max="40" value="18" />
            <span id="neutral-acid-value">18</span>
          </div>
        </label>
        <label>
          鹼的量
          <div class="slider-row">
            <span>0</span>
            <input id="neutral-base" type="range" min="0" max="40" value="18" />
            <span id="neutral-base-value">18</span>
          </div>
        </label>
      </div>
      <div class="lab-output" id="neutral-output"></div>
    </div>
  `;
  ["neutral-acid", "neutral-base"].forEach((id) => {
    document.getElementById(id).addEventListener("input", updateNeutralLab);
  });
  updateNeutralLab();
}

function updateNeutralLab() {
  const acid = Number(document.getElementById("neutral-acid").value);
  const base = Number(document.getElementById("neutral-base").value);
  setText("neutral-acid-value", acid);
  setText("neutral-base-value", base);
  const difference = acid - base;
  let result = "最接近完全中和";
  let note = "酸與鹼量相同，最接近剛好反應完。";

  if (difference > 0) {
    result = "偏酸";
    note = `酸比鹼多 ${difference} 單位，表示酸過量。`;
  } else if (difference < 0) {
    result = "偏鹼";
    note = `鹼比酸多 ${Math.abs(difference)} 單位，表示鹼過量。`;
  }

  document.getElementById("neutral-output").innerHTML = `
    <strong>模擬結果：${result}</strong>
    ${note}
  `;
}

function gradeQuiz() {
  const module = modules[state.currentModule];
  const answers = new FormData(quizForm);
  let score = 0;
  const explanations = [];

  module.quiz.forEach((item, index) => {
    const answer = answers.get(`question-${index}`);
    if (answer !== null && Number(answer) === item.answer) {
      score += 1;
    }
    explanations.push(
      `<div class="${Number(answer) === item.answer ? "result-good" : "result-warn"}">${index + 1}. ${item.explanation}</div>`
    );
  });

  const percent = Math.round((score / module.quiz.length) * 100);
  const previousBest = state.progress.bestScores[module.id] ?? 0;
  if (percent > previousBest) {
    state.progress.bestScores[module.id] = percent;
    saveProgress();
  }

  quizResult.innerHTML = `
    <strong>${module.title} 得分：${score} / ${module.quiz.length}（${percent}%）</strong>
    ${explanations.join("")}
  `;
  renderGuide();
}

function gradeSprintQuiz() {
  const answers = new FormData(sprintForm);
  let score = 0;
  const moduleMistakes = {};
  const explanations = [];

  state.sprintSet.forEach((item, index) => {
    const answer = answers.get(`sprint-question-${index}`);
    const correct = answer !== null && Number(answer) === item.answer;
    if (correct) {
      score += 1;
    } else {
      moduleMistakes[item.moduleTitle] = (moduleMistakes[item.moduleTitle] ?? 0) + 1;
    }
    explanations.push(
      `<div class="${correct ? "result-good" : "result-warn"}">${index + 1}. ${item.moduleTitle}：${item.explanation}</div>`
    );
  });

  const percent = Math.round((score / state.sprintSet.length) * 100);
  if (percent > state.progress.sprintBest) {
    state.progress.sprintBest = percent;
    saveProgress();
  }

  const weaknesses = Object.entries(moduleMistakes)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 2)
    .map(([title, count]) => `${title}（錯 ${count} 題）`);
  state.lastSprintSummary = weaknesses;
  renderSummary();

  sprintResult.innerHTML = `
    <div class="result-summary">
      <strong>段考衝刺快測：${score} / ${state.sprintSet.length}（${percent}%）</strong>
      ${
        weaknesses.length
          ? `優先補強：${weaknesses.join("、")}`
          : "這一回沒有明顯弱點，建議直接重做一回確認穩定度。"
      }
    </div>
    ${explanations.join("")}
  `;
  renderGuide();
}

function focusCurrentGuideTask() {
  const tasks = getGuideTasks(modules[state.currentModule]);
  const currentTask = tasks[Math.min(state.guideStep, tasks.length - 1)];
  startFocusTimer();
  focusTarget(currentTask.targetId);
}

function setText(id, value) {
  document.getElementById(id).textContent = value;
}

toggleComplete.addEventListener("click", () => {
  const module = modules[state.currentModule];
  const current = !!state.progress.completed[module.id];
  state.progress.completed[module.id] = !current;
  saveProgress();
  renderModule();
});

flashcard.addEventListener("click", () => {
  state.cardFlipped = !state.cardFlipped;
  renderFlashcard();
});

nextCard.addEventListener("click", () => {
  const module = modules[state.currentModule];
  state.cardIndex = (state.cardIndex + 1) % module.flashcards.length;
  state.cardFlipped = false;
  renderFlashcard();
});

submitQuiz.addEventListener("click", gradeQuiz);
submitSprint.addEventListener("click", gradeSprintQuiz);
toggleGuidedMode.addEventListener("click", () => {
  state.guidedMode = !state.guidedMode;
  renderGuidedMode();
});
toolTabs.forEach((tab) => {
  tab.addEventListener("click", () => {
    setActiveTool(tab.dataset.tool);
  });
});
guideAction.addEventListener("click", focusCurrentGuideTask);
guideDone.addEventListener("click", () => {
  const tasks = getGuideTasks(modules[state.currentModule]);
  stopFocusTimer();
  if (state.guideStep >= tasks.length - 1) {
    state.guideStep = 0;
  } else {
    state.guideStep += 1;
  }
  renderGuide();
});
guideEasier.addEventListener("click", () => {
  state.guideStep = Math.max(0, state.guideStep - 1);
  renderGuide();
  focusCurrentGuideTask();
});
regenSprint.addEventListener("click", () => {
  buildSprintSet();
  renderSprintQuiz();
});

startLearning.addEventListener("click", () => {
  document.getElementById("guide-panel").scrollIntoView({ behavior: "smooth", block: "start" });
  focusCurrentGuideTask();
});

jumpToSprint.addEventListener("click", () => {
  setActiveTool("sprint");
  document.getElementById("sprint-panel").scrollIntoView({ behavior: "smooth", block: "start" });
});

resetProgress.addEventListener("click", () => {
  state.progress = structuredClone(defaultProgress);
  state.lastSprintSummary = [];
  state.guideStep = 0;
  state.guidedMode = true;
  stopFocusTimer();
  buildSprintSet();
  renderSprintQuiz();
  saveProgress();
  renderModule();
});

buildSprintSet();
renderSprintQuiz();
renderSummary();
renderNav();
renderModule();
