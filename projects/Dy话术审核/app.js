const taxonomy = [
  {
    main: "食品饮料",
    children: [
      { first: "休闲食品", second: ["坚果炒货", "糕点点心", "肉类零食", "糖果巧克力", "饼干膨化"], keywords: ["坚果", "零食", "饼干", "糕点", "鸭脖", "牛肉干", "糖果"] },
      { first: "粮油调味", second: ["米面杂粮", "食用油", "调味品", "南北干货"], keywords: ["大米", "面粉", "食用油", "酱油", "调料", "木耳", "菌菇"] },
      { first: "饮料冲调", second: ["茶叶", "咖啡", "冲饮", "乳品饮料"], keywords: ["茶", "咖啡", "奶粉", "燕麦", "饮料", "冲泡"] },
      { first: "生鲜", second: ["水果", "肉禽蛋", "海鲜水产", "蔬菜", "预制菜"], keywords: ["水果", "牛肉", "羊肉", "海鲜", "鸡蛋", "预制菜"] },
    ],
  },
  {
    main: "家居日用",
    children: [
      { first: "厨房用品", second: ["保鲜袋", "收纳袋", "锅具", "餐具", "厨房小工具"], keywords: ["保鲜袋", "铝箔袋", "密封袋", "厨房", "锅", "筷子", "餐具", "砧板"] },
      { first: "家清纸品", second: ["纸巾", "清洁剂", "洗衣用品", "垃圾袋"], keywords: ["纸巾", "抽纸", "洗衣液", "清洁", "垃圾袋", "去污"] },
      { first: "收纳家装", second: ["收纳盒", "衣架", "浴室用品", "居家布艺"], keywords: ["收纳", "衣架", "浴室", "地垫", "床品", "置物架"] },
    ],
  },
  {
    main: "美妆个护",
    children: [
      { first: "护肤", second: ["面部护理", "身体护理", "防晒", "面膜"], keywords: ["精华", "面霜", "面膜", "防晒", "补水", "抗皱", "护肤"] },
      { first: "彩妆香水", second: ["口红", "底妆", "眼妆", "香水"], keywords: ["口红", "粉底", "气垫", "眼影", "睫毛", "香水"] },
      { first: "个人护理", second: ["洗发护发", "口腔护理", "身体清洁", "卫生巾"], keywords: ["洗发水", "护发素", "牙膏", "沐浴露", "卫生巾"] },
    ],
  },
  {
    main: "服饰鞋包",
    children: [
      { first: "女装", second: ["连衣裙", "上衣", "裤装", "内衣"], keywords: ["女装", "裙", "衬衫", "裤子", "内衣", "显瘦"] },
      { first: "男装", second: ["T恤", "衬衫", "外套", "裤装"], keywords: ["男装", "T恤", "外套", "夹克", "西裤"] },
      { first: "鞋包配饰", second: ["女鞋", "男鞋", "箱包", "饰品"], keywords: ["鞋", "包", "箱包", "项链", "耳环", "手表"] },
    ],
  },
  {
    main: "母婴宠物",
    children: [
      { first: "母婴用品", second: ["纸尿裤", "喂养用品", "童车童床", "孕产用品"], keywords: ["纸尿裤", "奶瓶", "婴儿", "宝宝", "孕妇", "童车"] },
      { first: "童装童鞋", second: ["童装", "童鞋", "儿童配饰"], keywords: ["童装", "童鞋", "儿童", "校服"] },
      { first: "宠物用品", second: ["宠物食品", "猫狗用品", "宠物清洁"], keywords: ["猫粮", "狗粮", "宠物", "猫砂", "牵引绳"] },
    ],
  },
  {
    main: "数码家电",
    children: [
      { first: "手机数码", second: ["手机配件", "耳机音箱", "智能设备", "摄影摄像"], keywords: ["手机壳", "耳机", "充电器", "数据线", "相机", "智能手表"] },
      { first: "生活电器", second: ["清洁电器", "厨房电器", "个护电器", "环境电器"], keywords: ["电饭煲", "空气炸锅", "吹风机", "吸尘器", "加湿器", "剃须刀"] },
      { first: "大家电", second: ["冰箱", "洗衣机", "空调", "电视"], keywords: ["冰箱", "洗衣机", "空调", "电视", "热水器"] },
    ],
  },
  {
    main: "运动户外",
    children: [
      { first: "运动装备", second: ["瑜伽健身", "跑步骑行", "球类运动", "运动护具"], keywords: ["瑜伽", "健身", "跑步", "骑行", "篮球", "护膝"] },
      { first: "户外出行", second: ["露营", "登山", "旅行装备", "户外服饰"], keywords: ["露营", "帐篷", "登山", "冲锋衣", "旅行"] },
    ],
  },
  {
    main: "本地生活与服务",
    children: [
      { first: "餐饮团购", second: ["套餐", "代金券", "茶饮甜品", "自助餐"], keywords: ["团购", "套餐", "代金券", "到店", "餐厅", "茶饮"] },
      { first: "酒旅休闲", second: ["酒店", "景区门票", "休闲娱乐", "丽人服务"], keywords: ["酒店", "门票", "景区", "按摩", "美甲", "美容院"] },
    ],
  },
  {
    main: "珠宝文玩",
    children: [
      { first: "珠宝首饰", second: ["黄金", "翡翠玉石", "珍珠", "银饰"], keywords: ["黄金", "翡翠", "玉", "珍珠", "银饰", "手镯"] },
      { first: "文玩收藏", second: ["茶器", "字画", "手串", "钱币邮票"], keywords: ["文玩", "手串", "字画", "茶器", "收藏"] },
    ],
  },
];

const complianceRules = [
  {
    id: "absolute-claims",
    title: "绝对化、唯一化、最优级表达",
    severity: "high",
    latest: "持续适用",
    basis: "直播宣传不得使用无法证明的最高级、绝对化、唯一化或排他性表达。",
    patterns: ["全网最低", "全国最低", "最低价", "第一", "唯一", "顶级", "最便宜", "最划算", "永久", "百分百", "100%", "绝对", "闭眼买", "天花板"],
    suggestion: "改成可被页面、活动或资质证明的表达，如“本场活动价”“主推款”“适合重点关注”。",
    replacements: { "全网最低": "本场活动价", "全国最低": "当前直播间到手价", "最低价": "活动价", "第一": "表现不错", "唯一": "主推", "顶级": "高规格", "最便宜": "价格更友好", "最划算": "性价比更突出", "永久": "按说明长期使用", "百分百": "尽量", "100%": "尽量", "绝对": "相对更", "闭眼买": "按需选择", "天花板": "高规格款" },
  },
  {
    id: "low-price-illusion",
    title: "虚假价格与低价错觉",
    severity: "high",
    latest: "2026-02 重点治理",
    basis: "不得通过虚构原价、补贴、同款对比、拆分价格或夸张话术制造低价错觉。",
    patterns: ["厂家直发", "没有中间商", "亏本", "赔钱", "平台补贴", "官方补贴", "别人卖", "线下卖", "原价", "专柜价", "到手不要", "一杯奶茶钱"],
    suggestion: "只讲页面可见价格、组合规则和优惠条件；对比价必须有明确证据。",
    replacements: { "厂家直发": "发货信息以订单页面为准", "没有中间商": "本场活动价", "亏本": "让利", "赔钱": "让利", "平台补贴": "本场优惠", "官方补贴": "本场优惠", "别人卖": "部分渠道价格", "线下卖": "部分渠道价格", "到手不要": "到手价为", "一杯奶茶钱": "价格门槛较低" },
  },
  {
    id: "marketing-gimmick",
    title: "违规营销噱头与虚假福利",
    severity: "high",
    latest: "2026-04 重点治理",
    basis: "不得使用虚假的清仓、倒闭、补贴、捡漏、内部价、限量福利等噱头误导成交。",
    patterns: ["清仓", "倒闭", "捡漏", "内部价", "老板疯了", "老板不在家", "亏哭", "福利款", "员工价", "尾货处理", "海关扣押", "撤柜"],
    suggestion: "活动原因、库存、优惠数量、赠品规则需要真实且与页面一致。",
    replacements: { "清仓": "本场活动", "倒闭": "本场活动", "捡漏": "重点关注", "内部价": "活动价", "老板疯了": "力度比较直接", "老板不在家": "本场福利", "亏哭": "让利", "福利款": "活动款", "员工价": "活动价", "尾货处理": "活动商品", "海关扣押": "现货商品", "撤柜": "活动商品" },
  },
  {
    id: "false-scarcity",
    title: "虚假限时、限量、倒计时",
    severity: "medium",
    latest: "2026-04 重点治理",
    basis: "限时、限量、库存、秒杀、活动结束等营销信息必须真实、明确、可核验。",
    patterns: ["最后1分钟", "最后 1 分钟", "最后一波", "错过再等一年", "再不拍就没了", "库存清空", "马上下架", "仅此一次", "手慢无", "抢光", "秒没"],
    suggestion: "改为“本轮活动即将结束”“库存以页面显示为准”“按需下单”。",
    replacements: { "最后1分钟": "本轮活动即将结束", "最后 1 分钟": "本轮活动即将结束", "最后一波": "本轮活动", "错过再等一年": "需要的朋友可以趁本场活动了解", "再不拍就没了": "库存以页面显示为准", "库存清空": "库存以购物车显示为准", "马上下架": "活动状态以页面为准", "仅此一次": "本场活动", "手慢无": "按需选择", "抢光": "库存以页面显示为准", "秒没": "库存变化较快" },
  },
  {
    id: "efficacy-medical",
    title: "功效夸大、医疗治疗暗示",
    severity: "high",
    latest: "持续适用",
    basis: "普通商品不得宣称治疗、预防疾病、改善身体指标等医疗或健康结果。",
    patterns: ["治疗", "治好", "根治", "降血糖", "降血压", "抗癌", "消炎", "排毒", "改善失眠", "去湿气", "调理体质", "抗敏", "修复屏障"],
    suggestion: "普通商品只描述成分、材质、使用感、适用场景和检测依据。",
    replacements: { "治疗": "日常护理", "治好": "辅助日常护理", "根治": "改善使用体验", "降血糖": "关注成分说明", "降血压": "关注成分说明", "抗癌": "关注成分说明", "消炎": "日常清洁", "排毒": "日常代谢相关感受", "改善失眠": "提升使用舒适度", "去湿气": "日常搭配", "调理体质": "适合日常使用", "抗敏": "温和护理", "修复屏障": "帮助维护肌肤状态" },
  },
  {
    id: "material-safety",
    title: "材质、安全、资质虚假",
    severity: "medium",
    latest: "持续适用",
    basis: "食品接触、无毒无味、婴童可用、孕妇可用、国家认证等表述必须有资质凭证。",
    patterns: ["食品级", "无毒", "无味", "婴儿可用", "孕妇可用", "国家认证", "官方认证", "绝对安全", "随便接触食物"],
    suggestion: "补充详情页材质、执行标准、检测报告；没有凭证时改为“按产品说明使用”。",
    replacements: { "食品级": "详情页标注的食品接触用材质", "无毒": "按说明使用更安心", "无味": "气味较轻", "婴儿可用": "家用场景可按需选择", "孕妇可用": "家用场景可按需选择", "国家认证": "详情页展示的资质信息", "官方认证": "详情页展示的资质信息", "绝对安全": "按说明使用更安心", "随便接触食物": "可按产品说明接触食物" },
  },
  {
    id: "spec-effect",
    title: "规格、容量、效果承诺不实",
    severity: "medium",
    latest: "持续适用",
    basis: "尺寸、容量、时长、防水、防潮、保鲜、承重等功能必须与商品实际规格一致。",
    patterns: ["放一个月", "永远不串味", "完全不漏", "什么都能装", "装多少都行", "一次买够一年", "万能", "用一辈子", "不坏"],
    suggestion: "改为使用场景和条件，如“短期冷藏收纳”“帮助减少串味”“按尺寸选择”。",
    replacements: { "放一个月": "短期冷藏收纳", "永远不串味": "帮助减少串味", "完全不漏": "正常使用下密封性较好", "什么都能装": "多种食材和小物都能收纳", "装多少都行": "按尺寸和重量选择", "一次买够一年": "一组满足一段时间使用", "万能": "多场景", "用一辈子": "耐用", "不坏": "更耐用" },
  },
  {
    id: "delivery-after-sale",
    title: "发货、到货、售后履约承诺",
    severity: "medium",
    latest: "持续适用",
    basis: "发货时效、到货时间、售后服务必须可履约，且与店铺和订单页面规则一致。",
    patterns: ["今天拍今天发", "明天必到", "包赔", "无条件退", "不用问客服", "一定能到", "马上发货", "破损包赔", "极速退款"],
    suggestion: "改为“符合条件会尽快安排”“物流以承运信息为准”“售后按页面规则处理”。",
    replacements: { "今天拍今天发": "符合发货条件的订单会尽快安排", "明天必到": "物流时效以承运信息为准", "包赔": "售后按店铺规则处理", "无条件退": "售后以页面规则为准", "不用问客服": "有问题可咨询客服", "一定能到": "物流以承运信息为准", "马上发货": "尽快安排发货", "破损包赔": "破损问题按售后规则处理", "极速退款": "退款以平台规则为准" },
  },
  {
    id: "fake-proof",
    title: "虚假评价、案例、销量数据背书",
    severity: "high",
    latest: "持续适用",
    basis: "不得编造用户评价、专家身份、检测数据、销量排行、复购排名或虚假案例。",
    patterns: ["十万好评", "专家推荐", "医生推荐", "央视同款", "销量第一", "复购第一", "人人都说好", "真实案例", "数据证明", "全网爆款"],
    suggestion: "只使用后台、详情页、资质文件中可证明的数据；无法证明时改为真实反馈型描述。",
    replacements: { "十万好评": "不少用户反馈", "专家推荐": "可以参考详情页说明", "医生推荐": "可以参考详情页说明", "央视同款": "同类型设计", "销量第一": "销量表现不错", "复购第一": "复购表现不错", "人人都说好": "不少用户反馈不错", "真实案例": "用户使用反馈", "数据证明": "详情页信息显示", "全网爆款": "热度较高的款" },
  },
  {
    id: "third-party-diversion",
    title: "诱导站外交易和私域导流",
    severity: "high",
    latest: "持续适用",
    basis: "不得诱导用户离开平台交易、添加站外联系方式或通过第三方链接完成交易。",
    patterns: ["加微信", "加薇", "私信发链接", "站外下单", "私下转账", "扫码付款", "进群领取", "跳转购买", "联系客服领大额券"],
    suggestion: "优惠、赠品、抽奖、售后和交易动作应通过平台工具、商品详情页或官方客服链路完成。",
    replacements: { "加微信": "通过店铺客服咨询", "加薇": "通过店铺客服咨询", "私信发链接": "在购物车页面查看", "站外下单": "通过平台订单下单", "私下转账": "通过平台订单支付", "扫码付款": "通过平台订单支付", "进群领取": "按页面活动规则领取", "跳转购买": "在购物车页面购买", "联系客服领大额券": "在页面按规则领取优惠" },
  },
  {
    id: "audience-pressure",
    title: "贬损、恐吓、过度施压",
    severity: "low",
    latest: "持续适用",
    basis: "直播间应避免羞辱、贬损、恐吓消费者或制造不适感。",
    patterns: ["不买就亏", "不会过日子", "傻", "别犹豫了", "不拍后悔", "家里人都该买", "活该"],
    suggestion: "改为尊重式提醒，强调适用人群、使用场景和自主选择。",
    replacements: { "不买就亏": "需要的朋友可以重点看", "不会过日子": "适合注重性价比的家庭", "傻": "不太合适", "别犹豫了": "按需选择", "不拍后悔": "需要可以先看规格", "家里人都该买": "适合多人家庭按需准备", "活该": "不太合适" },
  },
];

const segmentLabels = {
  opener: "开场/承接",
  pain: "痛点代入",
  proof: "卖点证明",
  spec: "规格选择",
  price: "价格福利",
  urgency: "收口催单",
  qa: "答疑补充",
};

const sampleScript = `咱这个中号和大号都能选，刚才好多姐姐问能不能装肉。来，我再说一遍，家里买回来的牛肉、鸡胸肉、孩子的水果辅食，不要直接用普通塑料袋塞冰箱。
普通袋子没有密封性，放一个月拿出来全是冰渣，还不健康。咱家这款铝箔保鲜袋，食品级材质，无毒无味，绝对安全，装肉、装水果、装辅食都可以。
它是拉链密封，正常冷藏分装更方便，南方回潮天也能做干货收纳。小号 20*13，中号 23*17，大号 26*27，买组合装更省心。
今天厂家直发，没有中间商，全网最低价，小号 9.9 米到手 50 个，中号 13.9 米到手 50 个，大号 15.9 米到手 30 个。
最后 1 分钟准备结束，错过再等一年，今天拍今天发，明天必到。不买就亏，闭眼买！`;

const state = {
  analysis: null,
  risks: [],
  optimized: "",
};

const $ = (selector) => document.querySelector(selector);

function escapeRegExp(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

function normalizeText(text) {
  return text.replace(/\r\n/g, "\n").replace(/[ \t]+/g, " ").trim();
}

function splitSentences(text) {
  return normalizeText(text)
    .split(/(?<=[。！？!?；;])|\n+/)
    .map((item) => item.trim())
    .filter(Boolean);
}

function scoreKeywords(text, keywords) {
  return keywords.reduce((sum, keyword) => sum + (text.includes(keyword) ? 1 : 0), 0);
}

function detectCategory(text) {
  let best = { score: 0, main: "其他综合", first: "待人工确认", second: "待人工确认", matched: [] };
  taxonomy.forEach((group) => {
    group.children.forEach((child) => {
      const matched = child.keywords.filter((keyword) => text.includes(keyword));
      const secondMatched = child.second.filter((name) => text.includes(name));
      const score = matched.length * 3 + secondMatched.length * 4;
      if (score > best.score) {
        best = {
          score,
          main: group.main,
          first: child.first,
          second: secondMatched[0] || child.second[0],
          matched: [...matched, ...secondMatched],
        };
      }
    });
  });
  return best;
}

function detectStyle(text) {
  const styleScores = [
    { name: "高燃成交型", score: scoreKeywords(text, ["来", "赶紧", "抓紧", "最后", "马上", "福利", "下单", "拍", "冲", "安排"]), reason: "催单词、节奏词、福利词密度高" },
    { name: "专业讲解型", score: scoreKeywords(text, ["材质", "规格", "结构", "检测", "标准", "成分", "详情页", "参数", "工艺", "适用"]), reason: "参数、材质、标准和证明表达较多" },
    { name: "温和种草型", score: scoreKeywords(text, ["适合", "舒服", "日常", "按需", "喜欢", "可以看看", "体验", "家用", "自用"]), reason: "体验、场景和按需选择表达较多" },
    { name: "答疑转化型", score: scoreKeywords(text, ["刚才", "问", "能不能", "怎么选", "几号", "客服", "看这里", "再说一遍"]), reason: "问答、复述和选择建议明显" },
  ];
  return styleScores.sort((a, b) => b.score - a.score)[0];
}

function detectSellingPoints(text) {
  const candidates = [
    "食品接触用材质", "铝箔", "密封", "拉链", "防潮", "防串味", "可复用", "大容量", "组合装", "便携", "收纳",
    "保湿", "温和", "显瘦", "透气", "速干", "低糖", "高蛋白", "新鲜", "现货", "赠品", "售后",
  ];
  const found = candidates.filter((item) => text.includes(item));
  const specMatches = text.match(/\d+\s?[*x×]\s?\d+|\d+\s?(个|只|片|斤|克|g|kg|ml|L|米|m)/gi) || [];
  return [...new Set([...found, ...specMatches])].slice(0, 10);
}

function detectProofs(text) {
  const proofWords = ["详情页", "检测报告", "质检", "执行标准", "资质", "证书", "订单页面", "购物车", "售后规则", "发货规则", "页面显示", "客服"];
  const found = proofWords.filter((item) => text.includes(item));
  if (found.length) return found;
  const inferred = [];
  if (/规格|尺寸|[0-9]\s?[*x×]\s?[0-9]/.test(text)) inferred.push("详情页规格");
  if (/材质|食品级|无毒|孕妇|婴儿/.test(text)) inferred.push("材质/检测资质待核验");
  if (/发货|到货|售后|退/.test(text)) inferred.push("订单页面和店铺规则待核验");
  if (/价格|到手|优惠|券|赠/.test(text)) inferred.push("活动页面价格规则待核验");
  return inferred.length ? inferred : ["未识别到明确凭证，需人工补充"];
}

function classifySegment(sentence) {
  if (/刚才|再说一遍|问|来看|听好|姐妹|哥哥|家人|朋友/.test(sentence)) return "opener";
  if (/痛点|普通|以前|麻烦|串味|回潮|浪费|不好|不方便|冰渣|脏|贵|难/.test(sentence)) return "pain";
  if (/材质|结构|成分|检测|标准|安全|密封|防潮|保鲜|工艺|详情页|资质/.test(sentence)) return "proof";
  if (/小号|中号|大号|规格|尺寸|[0-9]\s?[*x×]\s?[0-9]|多少|怎么选|组合/.test(sentence)) return "spec";
  if (/价格|到手|券|优惠|买|拍|赠|补贴|原价|活动价|米|元/.test(sentence)) return "price";
  if (/最后|抓紧|下单|库存|发货|售后|结束|错过|拍下|付/.test(sentence)) return "urgency";
  return "qa";
}

function detectRounds(sentences) {
  const segments = sentences.map((sentence, index) => ({ index, sentence, type: classifySegment(sentence) }));
  const starts = segments
    .filter((item) => ["opener", "pain", "proof"].includes(item.type))
    .map((item) => item.index);
  const start = starts[0] ?? 0;
  let end = segments.find((item) => item.index > start && item.type === "urgency")?.index ?? Math.min(sentences.length - 1, start + 8);
  if (end < start) end = sentences.length - 1;
  const selected = segments.filter((item) => item.index >= start && item.index <= end);
  const types = new Set(selected.map((item) => item.type));
  const missing = ["opener", "pain", "proof", "spec", "price", "urgency"].filter((type) => !types.has(type));
  const startsMidstream = segments[0]?.type !== "opener" && segments[0]?.type !== "pain";
  return { segments, selected, start, end, missing, startsMidstream };
}

function applyReplacements(text, rule) {
  let next = text;
  Object.entries(rule.replacements).forEach(([from, to]) => {
    next = next.replace(new RegExp(escapeRegExp(from), "g"), to);
  });
  return next;
}

function scanRisks(sentences) {
  const risks = [];
  sentences.forEach((sentence, sentenceIndex) => {
    complianceRules.forEach((rule) => {
      const matched = rule.patterns.filter((pattern) => sentence.includes(pattern));
      if (matched.length) {
        risks.push({
          rule,
          sentence,
          sentenceIndex,
          matched,
          rewrite: applyReplacements(sentence, rule),
        });
      }
    });
  });
  return risks;
}

function buildAnalysis(text) {
  const sentences = splitSentences(text);
  const category = detectCategory(text);
  const style = detectStyle(text);
  const sellingPoints = detectSellingPoints(text);
  const proofs = detectProofs(text);
  const round = detectRounds(sentences);
  return { sentences, category, style, sellingPoints, proofs, round };
}

function cleanSentence(sentence) {
  return complianceRules.reduce((current, rule) => applyReplacements(current, rule), sentence);
}

function sentenceByType(analysis, type) {
  return analysis.round.selected.filter((item) => item.type === type).map((item) => cleanSentence(item.sentence));
}

function buildOptimizedScript(analysis) {
  const { category, style, sellingPoints, proofs, round } = analysis;
  const points = sellingPoints.length ? sellingPoints.join("、") : "商品详情页展示的核心卖点";
  const proofText = proofs.join("、");
  const opening = round.startsMidstream
    ? `来，刚进来的朋友先听我把这一轮重点讲完整：这款属于${category.main} / ${category.first} / ${category.second}，适合关注${points}的朋友。`
    : (sentenceByType(analysis, "opener")[0] || `来，关注${points}的朋友可以先看这一款。`);

  const pain = sentenceByType(analysis, "pain");
  const proof = sentenceByType(analysis, "proof");
  const spec = sentenceByType(analysis, "spec");
  const price = sentenceByType(analysis, "price");
  const urgency = sentenceByType(analysis, "urgency");

  const blocks = [
    "【一轮优化话术】",
    `识别信息：${category.main} / ${category.first} / ${category.second}；主播风格：${style.name}；讲解依据：${proofText}。`,
    "",
    "一、开场承接",
    opening,
    "",
    "二、痛点代入",
    pain.length ? pain.join("\n") : `如果你正好有${category.second}相关的日常使用需求，可以先对照自己的场景看。`,
    "",
    "三、卖点证明",
    proof.length
      ? `${proof.join("\n")}\n涉及材质、安全、功效或效果的内容，直播中建议同步提醒“以详情页、检测/资质材料和产品说明为准”。`
      : `这款重点围绕${points}来讲，具体材质、规格、适用范围以详情页和资质材料为准。`,
    "",
    "四、规格选择",
    spec.length ? spec.join("\n") : "规格、数量、尺寸和组合以购物车页面展示为准；不确定的朋友可以先按使用场景选择。",
    "",
    "五、价格福利",
    price.length
      ? `${price.join("\n")}\n价格、优惠、赠品和组合规则以直播间页面展示为准，不做全网最低、亏本补贴等无法证明的承诺。`
      : "本场价格和优惠以页面展示为准，需要的朋友可以先看购物车规格和到手价。",
    "",
    "六、合规收口",
    urgency.length
      ? `${urgency.join("\n")}\n下单前请核对规格、数量、发货和售后规则；库存和活动时间以页面显示为准，按需选择。`
      : "需要的朋友按自己的使用场景和预算选择，活动、库存、发货和售后都以页面显示为准。",
  ];

  if (round.missing.length) {
    blocks.push("", `【缺失环节提醒】当前录音缺少：${round.missing.map((type) => segmentLabels[type]).join("、")}。已在优化稿中补了合规承接句。`);
  }

  return blocks.join("\n");
}

function getScore(risks) {
  const penalty = risks.reduce((sum, item) => {
    if (item.rule.severity === "high") return sum + 13;
    if (item.rule.severity === "medium") return sum + 8;
    return sum + 4;
  }, 0);
  return Math.max(0, Math.min(100, 100 - penalty));
}

function scoreLabel(score) {
  if (score >= 86) return "风险较低，复核凭证后可播";
  if (score >= 70) return "需要小幅修改";
  if (score >= 50) return "存在明显违规风险";
  return "高风险，建议重写";
}

function severityName(severity) {
  return { high: "高风险", medium: "中风险", low: "低风险" }[severity];
}

function auditScript() {
  const text = $("#scriptInput").value.trim();
  if (!text) {
    alert("请先粘贴或上传需要审核的话术 TXT。");
    return;
  }
  const analysis = buildAnalysis(text);
  const risks = scanRisks(analysis.sentences);
  state.analysis = analysis;
  state.risks = risks;
  state.optimized = buildOptimizedScript(analysis);
  renderAudit();
}

function renderAnalysis() {
  const { category, style, sellingPoints, proofs, round } = state.analysis;
  $("#detectedCategory").textContent = category.second === "待人工确认" ? "未识别到明确商品类目" : category.second;
  $("#categoryPath").textContent = `${category.main} / ${category.first} / ${category.second}（命中：${category.matched.join("、") || "无"}）`;
  $("#detectedStyle").textContent = style.name;
  $("#styleReason").textContent = style.reason;
  $("#detectedSellingPoints").textContent = sellingPoints.length ? sellingPoints.join("、") : "未识别到明确卖点";
  $("#detectedProofs").textContent = proofs.join("、");
  $("#roundCount").textContent = round.selected.length ? 1 : 0;
  $("#segmentCount").textContent = new Set(round.selected.map((item) => item.type)).size;
}

function renderRoundMap() {
  const { round } = state.analysis;
  const selectedIndexes = new Set(round.selected.map((item) => item.index));
  $("#roundMap").innerHTML = `
    <div class="round-summary">
      <strong>识别范围：第 ${round.start + 1} 句至第 ${round.end + 1} 句</strong>
      <span>${round.startsMidstream ? "录音疑似从中段开始，已补开场承接。" : "包含自然开场或承接句。"}</span>
      <span>${round.missing.length ? `缺失：${round.missing.map((type) => segmentLabels[type]).join("、")}` : "结构完整度较好。"}</span>
    </div>
    <div class="segment-list">
      ${round.segments
        .map(
          (item) => `
            <article class="${selectedIndexes.has(item.index) ? "selected" : ""}">
              <span>${item.index + 1}. ${segmentLabels[item.type]}</span>
              <p>${item.sentence}</p>
            </article>
          `
        )
        .join("")}
    </div>
  `;
}

function renderRisks() {
  if (!state.risks.length) {
    $("#riskList").innerHTML = '<div class="empty-state">未命中高频风险词，但仍需人工核对详情页、价格活动、资质和履约规则。</div>';
    return;
  }
  $("#riskList").innerHTML = state.risks
    .map(
      (item) => `
        <article class="risk-item ${item.rule.severity}">
          <div class="risk-head">
            <strong>${item.rule.title}</strong>
            <span class="badge ${item.rule.severity}">${severityName(item.rule.severity)}</span>
          </div>
          <p class="quote">原句：${item.sentence}</p>
          <p>命中词：${item.matched.join("、")}</p>
          <p>最新口径：${item.rule.latest}</p>
          <p>规则依据：${item.rule.basis}</p>
          <p>建议：${item.rule.suggestion}</p>
          <p class="quote">建议改写：${item.rewrite}</p>
        </article>
      `
    )
    .join("");
}

function renderAudit() {
  renderAnalysis();
  renderRoundMap();
  renderRisks();
  const score = getScore(state.risks);
  $("#scoreValue").textContent = score;
  $("#scoreLabel").textContent = scoreLabel(score);
  $("#riskCount").textContent = state.risks.length;
  $("#highCount").textContent = state.risks.filter((item) => item.rule.severity === "high").length;
  $("#optimizedOutput").textContent = state.optimized;
}

function renderRules(filter = "") {
  const value = filter.trim();
  const rules = complianceRules.filter((rule) => {
    if (!value) return true;
    return [rule.title, rule.latest, rule.basis, rule.suggestion, ...rule.patterns].some((item) => item.includes(value));
  });
  $("#rulesGrid").innerHTML = rules
    .map(
      (rule) => `
        <article>
          <div class="rule-head">
            <h4>${rule.title}</h4>
            <span class="badge ${rule.severity}">${severityName(rule.severity)}</span>
          </div>
          <p><strong>口径：</strong>${rule.latest}</p>
          <p>${rule.basis}</p>
          <p>${rule.suggestion}</p>
          <ul>${rule.patterns.slice(0, 10).map((pattern) => `<li>${pattern}</li>`).join("")}</ul>
        </article>
      `
    )
    .join("");
}

function renderTaxonomy(filter = "") {
  const value = filter.trim();
  const cards = [];
  taxonomy.forEach((group) => {
    group.children.forEach((child) => {
      const haystack = [group.main, child.first, ...child.second, ...child.keywords].join(" ");
      if (!value || haystack.includes(value)) {
        cards.push(`
          <article>
            <span>${group.main}</span>
            <h4>${child.first}</h4>
            <p>${child.second.join(" / ")}</p>
            <small>识别词：${child.keywords.join("、")}</small>
          </article>
        `);
      }
    });
  });
  $("#taxonomyGrid").innerHTML = cards.join("");
}

function exportReport() {
  if (!state.optimized || !state.analysis) {
    alert("请先完成一次审核。");
    return;
  }
  const { category, style, sellingPoints, proofs, round } = state.analysis;
  const report = [
    "抖音直播话术审核报告",
    `生成时间：${new Date().toLocaleString("zh-CN")}`,
    `类目：${category.main} / ${category.first} / ${category.second}`,
    `主播风格：${style.name}`,
    `核心卖点：${sellingPoints.join("、") || "未识别"}`,
    `事实凭证：${proofs.join("、")}`,
    `一轮话术：第 ${round.start + 1} 句至第 ${round.end + 1} 句`,
    `合规评分：${$("#scoreValue").textContent}`,
    `风险命中：${state.risks.length}`,
    "",
    "一、风险明细",
    ...state.risks.map((item, index) => `${index + 1}. ${severityName(item.rule.severity)}｜${item.rule.title}\n原句：${item.sentence}\n命中词：${item.matched.join("、")}\n建议：${item.rule.suggestion}\n`),
    "",
    "二、整理优化稿",
    state.optimized,
  ].join("\n");
  const blob = new Blob([report], { type: "text/plain;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = `话术审核报告-${Date.now()}.txt`;
  link.click();
  URL.revokeObjectURL(url);
}

function bindEvents() {
  $("#auditBtn").addEventListener("click", auditScript);
  $("#sampleBtn").addEventListener("click", () => {
    $("#scriptInput").value = sampleScript;
    auditScript();
  });
  $("#copyBtn").addEventListener("click", async () => {
    if (!state.optimized) return;
    await navigator.clipboard.writeText(state.optimized);
    $("#copyBtn").textContent = "已复制";
    window.setTimeout(() => ($("#copyBtn").textContent = "复制优化稿"), 1400);
  });
  $("#exportBtn").addEventListener("click", exportReport);
  $("#ruleSearch").addEventListener("input", (event) => renderRules(event.target.value));
  $("#taxonomySearch").addEventListener("input", (event) => renderTaxonomy(event.target.value));
  $("#fileInput").addEventListener("change", async (event) => {
    const file = event.target.files?.[0];
    if (!file) return;
    $("#scriptInput").value = await file.text();
    auditScript();
  });
  document.querySelectorAll(".nav-item").forEach((button) => {
    button.addEventListener("click", () => {
      document.querySelectorAll(".nav-item").forEach((item) => item.classList.remove("active"));
      document.querySelectorAll(".section-view").forEach((section) => section.classList.remove("active"));
      button.classList.add("active");
      $(`#${button.dataset.section}`).classList.add("active");
    });
  });
}

renderRules();
renderTaxonomy();
bindEvents();
