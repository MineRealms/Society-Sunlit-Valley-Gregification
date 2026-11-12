// Sunlit Valley 统一状态面板（需要 sunlithud 模组）
// 面板在服务端声明，模组会把它同步给客户端；/reload 后自动重新声明并重发。
// 位置/内容都可以直接改这里，不需要重启游戏。

(function () {
  if (typeof SunlitHud === 'undefined') {
    console.info('[Sunlit] sunlithud 模组未安装，HUD 已跳过')
    return
  }

  const NUTRIENTS = [
    ['dairy', '乳'],
    ['fruit', '果'],
    ['grain', '谷'],
    ['protein', '蛋白'],
    ['vegetable', '菜']
  ]

  // 区块污染值：Pollution 的服务端权威 API（api.pollution 包，专用服亦存在）。
  // 缓存类引用一次；缺失时降级为 "—"，绝不让脚本崩。
  let PollutionEngine = null
  try {
    PollutionEngine = Java.loadClass('meowmel.pollution.api.pollution.PollutionEngine')
  } catch (err) {
    console.info('[Sunlit] Pollution 未安装，区块污染值显示为 —')
  }

  const fmtVal = (v) => {
    let n = Number(v)
    if (!isFinite(n)) return '—'
    return Math.round(n) === n ? String(Math.round(n)) : n.toFixed(1)
  }

  const hasProviders = (() => {
    try { return typeof SunlitHud.provider === 'function' } catch (err) { return false }
  })()

  // 「扭曲 + 区块污染」合并成一行：扭曲复用 mod 内置的服务端 snapshot，
  // 污染用 PollutionEngine.get(ServerLevel, BlockPos) 取当前区块权威值。
  // provider 每秒在服务端采样，结果经 DataMessage 同步给客户端。
  if (hasProviders) {
    SunlitHud.provider('society.warp_pollution', (player) => {
      let warp = 0
      try {
        let snap = SunlitHud.snapshot(player)
        let w = snap && snap.get ? snap.get('warpTotal') : (snap ? snap.warpTotal : 0)
        warp = Number(w)
        if (!isFinite(warp)) warp = 0
      } catch (err) {}

      let pollution = '—'
      if (PollutionEngine) {
        try {
          pollution = fmtVal(PollutionEngine.get(player.level, player.blockPosition()))
        } catch (err) {}
      }
      return '扭曲 ' + fmtVal(warp) + ' · 污染 ' + pollution
    })
  }

  const rows = [
    { type: 'text', source: 'day', color: '#FFD37F' },
    { type: 'text', source: 'season', label: '季节', color: '#8FD9FF' },
    // 下面三行全部由客户端直接读取，不需要服务端同步
    { type: 'text', source: 'dimension', label: '世界', color: '#A7D8FF' },
    { type: 'text', source: 'xyz', label: '坐标', color: '#E8E8E8' },
    { type: 'text', source: 'biome', label: '群系', color: '#A8E6A1' }
  ]

  for (const [key, label] of NUTRIENTS) {
    rows.push({
      type: 'bar',
      source: 'nutrient.' + key,
      label: label,
      barMax: 30,
      color: '#9BD47A'
    })
  }

  // 扭曲 + 区块污染合并成一栏，默认常显（不设 hideBelow/hideAbove）。
  // 旧版 sunlithud 无 provider 时退回两个独立行，同样常显。
  if (hasProviders) {
    rows.push({ type: 'text', source: 'society.warp_pollution', color: '#C77DFF' })
  } else {
    rows.push(
      { type: 'text', source: 'warp.total', label: '扭曲', color: '#C77DFF' },
      { type: 'text', source: 'pollution', label: '污染', color: '#B8B8B8' }
    )
  }
  rows.push({ type: 'text', source: 'light', label: '光照', hideAbove: 7, color: '#FFE066' })

  let panels = []
  try {
    let current = JSON.parse(SunlitHud.json())
    if (Array.isArray(current)) panels = current.filter((panel) => panel && panel.id !== 'sunlit_status')
  } catch (err) {
    console.warn('[Sunlit] 读取现有 HUD 面板失败，重新声明状态面板: ' + err)
  }
  panels.push({
    id: 'sunlit_status',
    anchor: 'top_left',
    x: 4,
    y: 4,
    width: 118,
    scale: 1.0,
    rows: rows
  })
  SunlitHud.panels(panels)

  console.info('[Sunlit] HUD 面板已声明')
})()
