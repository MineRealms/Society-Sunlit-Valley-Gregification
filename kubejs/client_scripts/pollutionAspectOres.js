ItemEvents.tooltip(event => {
  event.add(/^(pollution|gtceu):(.*_)?infused_(air|earth|entropy|fire|order|water)_ore$/,
    Text.translate("tooltip.sunlitindustry.no_player_harvest"))
})
