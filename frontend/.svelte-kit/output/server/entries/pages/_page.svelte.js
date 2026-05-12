import { e as escape_html, a0 as ensure_array_like, a1 as attr_class, a2 as stringify, a3 as attr } from "../../chunks/renderer.js";
function _page($$renderer, $$props) {
  $$renderer.component(($$renderer2) => {
    let messages = [];
    let input = "";
    let systemPrompt = "";
    let isStreaming = false;
    $$renderer2.push(`<div class="chat-container svelte-1uha8ag"><div class="system-prompt-container svelte-1uha8ag"><details><summary>System Prompt</summary> <textarea placeholder="Enter system instructions..." class="svelte-1uha8ag">`);
    const $$body = escape_html(systemPrompt);
    if ($$body) {
      $$renderer2.push(`${$$body}`);
    }
    $$renderer2.push(`</textarea></details></div> <div class="messages-area svelte-1uha8ag"><!--[-->`);
    const each_array = ensure_array_like(messages);
    for (let $$index = 0, $$length = each_array.length; $$index < $$length; $$index++) {
      let message = each_array[$$index];
      $$renderer2.push(`<div${attr_class(`message-wrapper ${stringify(message.role)}`, "svelte-1uha8ag")}><div class="message-bubble svelte-1uha8ag">${escape_html(message.content)}</div></div>`);
    }
    $$renderer2.push(`<!--]--></div> <div class="input-area svelte-1uha8ag"><form class="svelte-1uha8ag"><input type="text"${attr("value", input)} placeholder="Type a message..."${attr("disabled", isStreaming, true)} class="svelte-1uha8ag"/> <button type="submit"${attr("disabled", !input.trim(), true)} class="svelte-1uha8ag">${escape_html("Send")}</button></form></div></div>`);
  });
}
export {
  _page as default
};
