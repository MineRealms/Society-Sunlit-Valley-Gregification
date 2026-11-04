// priority: 9
// ============================================================
// SunlitMarket 面板（需要 sunlithud 模组）
//
// SunlitHud.panels() 是整体替换，所以这里不直接声明自己的面板，
// 而是读回当前面板表、去掉旧的 sunlitmarket 面板、再追加一块，
// 这样和 sunlitHud.js 的营养/季节面板共存，重复 /reload 也不会叠加。
// 数据源每秒在服务端采样一次，再同步给客户端。
// ============================================================
if (typeof SunlitHud !== 'undefined' && typeof SunlitMarket !== 'undefined') {
  let PANEL_ID = 'sunlitmarket'

  // 服务端的 sunlithud 可能还是没有 provider API 的旧版。那种情况下整块面板
  // 只会显示空行，不如直接跳过（避免脚本报错，也避免误导玩家）。
  let hasProviders = false
  try {
    hasProviders = typeof SunlitHud.provider === 'function'
  } catch (err) {
    hasProviders = false
  }
  if (!hasProviders) {
    console.info('[SV-INTEGRATION] sunlithud 无 provider API（旧版），HUD 面板跳过')
  }

  if (hasProviders) SunlitHud.provider('sm.balance', (player) => SunlitMarket.balance(player))
  if (hasProviders) SunlitHud.provider('sm.wanted', (player) => SunlitMarket.wanted(player))
  if (hasProviders) SunlitHud.provider('sm.title', (player) => {
    let faction = SunlitMarket.topFaction(player)
    return faction ? SunlitMarket.title(player, faction) : '中立'
  })

  let declare = () => {
    let panels = []
    try {
      let raw = JSON.parse(SunlitHud.json())
      if (Array.isArray(raw)) panels = raw.filter((panel) => panel && panel.id !== PANEL_ID)
    } catch (err) {
      panels = []
    }
    panels.push({
      id: PANEL_ID,
      anchor: 'bottom_left',
      x: 4,
      y: 4,
      width: 96,
      scale: 1.0,
      rows: [
        { type: 'text', source: 'sm.balance', label: '余额', color: '#FFD37F' },
        { type: 'text', source: 'sm.title', label: '结盟', color: '#8FD9FF' },
        { type: 'text', source: 'sm.wanted', label: '通缉', hideBelow: 1, color: '#FF7B7B' }
      ]
    })
    SunlitHud.panels(panels)
  }

  // 加载时先声明一次（脚本重载即刻生效），loaded 再声明一次，
  // 保证和 sunlitHud.js 的加载顺序无关。
  if (hasProviders) {
    declare()
    ServerEvents.loaded((event) => declare())
    console.info('[SV-INTEGRATION] SunlitMarket HUD panel declared')
  }
}
