// priority: -1000
(function () {
  var LOG = '[SUNLIT-INFUSION] ';
  var RESEARCH = 'pollution.magic.thaumcraft_research';

  function positive(value, maximum) {
    if (typeof value !== 'number' || Math.floor(value) !== value || value < 1 || value > maximum) throw new Error('invalid amount: ' + value);
    return value;
  }

  function knownFields(value, allowed) {
    if (!value || typeof value !== 'object' || Array.isArray(value)) throw new Error('expected object');
    Object.keys(value).forEach(function (key) {
      if (allowed.indexOf(key) < 0) throw new Error('unsupported field: ' + key);
    });
  }

  function input(value) {
    knownFields(value, ['item', 'tag', 'count']);
    if ((typeof value.item === 'string') === (typeof value.tag === 'string')) throw new Error('expected one item or tag');
    var id = value.item || value.tag;
    if (!/^[a-z0-9_.-]+:[a-z0-9_./-]+$/.test(id)) throw new Error('invalid input id');
    return {id: id, tag: !!value.tag, count: positive(value.count === undefined ? 1 : value.count, 64)};
  }

  function industrial(recipe, policy, fluids) {
    knownFields(recipe, ['type', 'research', 'central', 'components', 'instability', 'aspects', 'result', 'conditions', 'group', 'category']);
    if (recipe.type !== 'thaumcraft:infusion') throw new Error('not ordinary infusion');
    if (recipe.research !== undefined && typeof recipe.research !== 'string') throw new Error('unsupported research');
    if (!Array.isArray(recipe.components) || !recipe.components.length) throw new Error('missing components');
    knownFields(recipe.result, ['item', 'count', 'nbt']);
    if (typeof recipe.result.item !== 'string') throw new Error('missing output');
    if (recipe.result.nbt !== undefined && typeof recipe.result.nbt !== 'string') throw new Error('unsupported output NBT');
    var inputs = [input(recipe.central)].concat(recipe.components.map(input));
    if (inputs.length > 25) throw new Error('more than 25 item inputs');
    var merged = {}, total = 0;
    knownFields(recipe.aspects, Object.keys(recipe.aspects || {}));
    Object.keys(recipe.aspects).forEach(function (aspect) {
      var amount = positive(recipe.aspects[aspect], 1000000);
      var key = aspect.indexOf(':') < 0 ? aspect : aspect.replace(/^thaumcraft:/, '');
      if (!fluids[key]) throw new Error('unmapped aspect: ' + aspect);
      merged[fluids[key]] = (merged[fluids[key]] || 0) + amount * 144;
      if (merged[fluids[key]] > 2147483647) throw new Error('fluid amount overflow');
      total += amount;
    });
    if (Object.keys(merged).length > 8) throw new Error('more than 8 fluid inputs');
    var eut = positive(policy.eut, 2147483647);
    return {inputs: inputs, fluids: merged, result: recipe.result.item,
      count: positive(recipe.result.count === undefined ? 1 : recipe.result.count, 64),
      nbt: recipe.result.nbt || null, research: recipe.research || '', duration: Math.max(100, total * 5), eut: eut};
  }

  function awaken(recipe, policy) {
    if (recipe.type !== 'thaumcraft:infusion' || recipe.central.item !== policy.central || recipe.result.item !== policy.output) {
      throw new Error('upstream awakening definition changed');
    }
    var result = JSON.parse(JSON.stringify(recipe));
    policy.additions.forEach(function (addition) {
      var part = input(addition);
      if (part.tag) throw new Error('boss material must be an exact item');
      for (var i = 0; i < part.count; i++) result.components.push({item: part.id});
    });
    if (result.components.length > 32) throw new Error('too many pedestal components');
    return result;
  }

  function legacyId(id) {
    return 'pollution:industrial_infusion_recipes/industrial_infusion/thaumic/' + id.replace(':', '/recipes/');
  }

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = {industrial: industrial, awaken: awaken, legacyId: legacyId};
  }
  if (typeof ServerEvents === 'undefined') return;

  ServerEvents.recipes(function (event) {
    if (!Platform.isLoaded('thaumcraft')) return;
    var boss = JSON.parse(String(JsonIO.readString('kubejs/config/sunlit-boss-awakening.json')));
    var common = JSON.parse(String(JsonIO.readString('kubejs/config/sunlit-industrial-infusion.json')));
    if (!boss || !common) throw new Error(LOG + 'missing policy JSON');
    // The event has already applied ordinary pack recipe edits. Copy these live definitions.
    function definition(id) {
      var found = null;
      function read(recipe) {
        if (recipe.removed || String(recipe.getId()) !== id) return;
        recipe.serialize();
        found = JSON.parse(recipe.json.toString());
      }
      event.forEachRecipe({id: id}, read);
      // KubeJS build 16's forEachRecipe only visits originalRecipes.
      event.addedRecipes.forEach(read);
      return found;
    }
    function remove(id) {
      event.remove({id: id});
      event.addedRecipes.forEach(function (recipe) {
        if (!recipe.removed && String(recipe.getId()) === id) recipe.remove();
      });
    }

    var patched = 0, converted = 0, skipped = 0;
    if (boss.enabled && Platform.isLoaded('cataclysm') && Platform.isLoaded('thaumictinkerer')) {
      Object.keys(boss.recipes).forEach(function (id) {
        var original = definition(id);
        if (!original) { console.warn(LOG + 'missing awakening source: ' + id); return; }
        var changed = awaken(original, boss.recipes[id]);
        remove(id);
        event.custom(changed).id(id);
        // A future Pollution whitelist addition must not reintroduce the unmodified JAR route.
        remove(legacyId(id));
        patched++;
      });
    }

    if (common.enabled && Platform.isLoaded('pollution')) {
      var Mapping = Java.loadClass('meowmel.pollution.api.magic.PollutionAspectMapping');
      var fluids = {};
      Mapping.all().forEach(function (material, aspect) {
        var stack = material.getFluid(1);
        if (!stack.isEmpty()) fluids[String(aspect.serialized()).replace(/^thaumcraft:/, '')] = String(Fluid.getId(stack.getFluid()));
      });
      Object.keys(common.recipes).forEach(function (id) {
        // Remove the JAR twin even if the live TC recipe was removed or became unsupported.
        remove(legacyId(id));
        var original = definition(id);
        if (!original) { skipped++; console.warn(LOG + 'missing industrial source: ' + id); return; }
        var generated = null;
        try {
          var row = industrial(original, common.recipes[id], fluids);
          row.inputs.forEach(function (part) {
            if (!part.tag && Item.of(part.id).hasCraftingRemainingItem()) throw new Error('container input: ' + part.id);
          });
          generated = event.recipes.gtceu.industrial_infusion_recipes('society:industrial_infusion/' + id.replace(':', '/'));
          row.inputs.forEach(function (part) { generated.itemInputs(String(part.count + 'x ' + (part.tag ? '#' : '') + part.id)); });
          Object.keys(row.fluids).forEach(function (fluid) { generated.inputFluids(Fluid.of(fluid, row.fluids[fluid])); });
          generated.itemOutputs(row.nbt ? Item.of(row.result, row.count, row.nbt) : row.count + 'x ' + row.result).duration(row.duration).EUt(row.eut);
          if (row.research) generated.addDataString(RESEARCH, row.research);
          converted++;
        } catch (error) {
          if (generated) generated.remove();
          skipped++;
          console.warn(LOG + 'skipped ' + id + ': ' + error);
        }
      });
    }
    console.info(LOG + 'awakening=' + patched + ' industrial=' + converted + ' skipped=' + skipped);
  });
})();
