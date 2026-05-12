export const manifest = (() => {
function __memo(fn) {
	let value;
	return () => value ??= (value = fn());
}

return {
	appDir: "_app",
	appPath: "_app",
	assets: new Set([".gitkeep"]),
	mimeTypes: {},
	_: {
		client: {start:"_app/immutable/entry/start.DRwhnwsX.js",app:"_app/immutable/entry/app.CL0YBrr6.js",imports:["_app/immutable/entry/start.DRwhnwsX.js","_app/immutable/chunks/BCT-nXPL.js","_app/immutable/chunks/QdolyXNc.js","_app/immutable/chunks/Rx157xrw.js","_app/immutable/entry/app.CL0YBrr6.js","_app/immutable/chunks/QdolyXNc.js","_app/immutable/chunks/2qzLpJc9.js","_app/immutable/chunks/CARvktBR.js","_app/immutable/chunks/Rx157xrw.js","_app/immutable/chunks/dv5alIKU.js","_app/immutable/chunks/DW-5IErj.js"],stylesheets:[],fonts:[],uses_env_dynamic_public:false},
		nodes: [
			__memo(() => import('./nodes/0.js')),
			__memo(() => import('./nodes/1.js')),
			__memo(() => import('./nodes/2.js'))
		],
		remotes: {
			
		},
		routes: [
			{
				id: "/",
				pattern: /^\/$/,
				params: [],
				page: { layouts: [0,], errors: [1,], leaf: 2 },
				endpoint: null
			}
		],
		prerendered_routes: new Set([]),
		matchers: async () => {
			
			return {  };
		},
		server_assets: {}
	}
}
})();
