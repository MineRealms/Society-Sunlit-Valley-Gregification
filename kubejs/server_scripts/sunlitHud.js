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

  rows.push(
    { type: 'text', source: 'warp.total', label: '扭曲', hideBelow: 1, color: '#C77DFF' },
    { type: 'text', source: 'light', label: '光照', hideAbove: 7, color: '#FFE066' },
    { type: 'text', source: 'pollution', label: '污染', hideBelow: 1, color: '#B8B8B8' }
  )

  SunlitHud.panels([{
    id: 'sunlit_status',
    anchor: 'top_left',
    x: 4,
    y: 4,
    width: 118,
    scale: 1.0,
    rows: rows
  }])

  console.info('[Sunlit] HUD 面板已声明')
})()
