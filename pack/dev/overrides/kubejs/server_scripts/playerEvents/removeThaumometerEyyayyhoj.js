// Temporary fix: Remove Thaumometer from eyyayyhoj on login to prevent Thaumcraft crash
// Crash: ObjectStatePlatform.store - Thaumometer's ObjectState capability missing
// Remove this file once Thaumcraft is updated to 20731+ (which fixes the bug)

PlayerEvents.loggedIn(event => {
    const player = event.player
    if (player.username == "eyyayyhoj") {
        // Remove Thaumometer from all inventory slots
        let removed = 0
        for (let i = 0; i < player.inventory.size(); i++) {
            const stack = player.inventory.getStackInSlot(i)
            if (!stack.isEmpty() && stack.id == "thaumcraft:thaumometer") {
                player.inventory.setStackInSlot(i, ItemStack.EMPTY)
                removed++
            }
        }
        // Also check offhand
        const offhand = player.offhandItem
        if (!offhand.isEmpty() && offhand.id == "thaumcraft:thaumometer") {
            player.setItemInHand(InteractionHand.OFF_HAND, ItemStack.EMPTY)
            removed++
        }
        // Also check armor slots
        for (let i = 0; i < player.armor.length; i++) {
            const stack = player.armor[i]
            if (!stack.isEmpty() && stack.id == "thaumcraft:thaumometer") {
                player.armor[i] = ItemStack.EMPTY
                removed++
            }
        }
        if (removed > 0) {
            console.info(`[ThaumometerFix] Removed ${removed} Thaumometer(s) from eyyayyhoj on login`)
        }
    }
})