

export const index = 0;
let component_cache;
export const component = async () => component_cache ??= (await import('../entries/fallbacks/layout.svelte.js')).default;
export const imports = ["_app/immutable/nodes/0.Bg395tYA.js","_app/immutable/chunks/CARvktBR.js","_app/immutable/chunks/QdolyXNc.js","_app/immutable/chunks/dv5alIKU.js"];
export const stylesheets = [];
export const fonts = [];
