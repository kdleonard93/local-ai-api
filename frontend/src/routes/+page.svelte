<script lang="ts">

  interface Message {
    role: 'user' | 'assistant';
    content: string;
  }

  let messages: Message[] = [];
  let input = '';
  let systemPrompt = '';
  let isStreaming = false;
  let scrollContainer: HTMLDivElement;

  // Hardcoded API key for dev
  const API_KEY = 'dev-key';
  const API_URL = 'http://localhost:8000/v1/chat';

  async function sendMessage() {
    if (!input.trim() || isStreaming) return;

    const userMessage: Message = { role: 'user', content: input };
    messages = [...messages, userMessage];
    const currentInput = input;
    input = '';
    isStreaming = true;

    // Add placeholder for assistant message
    const assistantMessageIndex = messages.length;
    messages = [...messages, { role: 'assistant', content: '' }];

    try {
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-API-Key': API_KEY
        },
        body: JSON.stringify({
          prompt: currentInput,
          system: systemPrompt || undefined,
          model: undefined // use default
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const reader = response.body?.getReader();
      const decoder = new TextDecoder();
      
      if (!reader) throw new Error('No reader available');

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });
        const lines = chunk.split('\n\n');

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const content = line.replace('data: ', '').trim();
            
            if (content === '[DONE]') {
              isStreaming = false;
              break;
            }

            if (content.startsWith('Error: ')) {
              throw new Error(content.substring(7));
            }

            // Reassign to trigger Svelte reactivity
            messages[assistantMessageIndex] = {
              ...messages[assistantMessageIndex],
              content: messages[assistantMessageIndex].content + content
            };
            messages = messages;
          }
        }
        
        // Scroll to bottom
        if (scrollContainer) {
          scrollContainer.scrollTop = scrollContainer.scrollHeight;
        }
      }
    } catch (error) {
      console.error('Error streaming:', error);
      messages[assistantMessageIndex].content = 'Error: ' + (error instanceof Error ? error.message : 'Unknown error');
      isStreaming = false;
    } finally {
      isStreaming = false;
      // Ensure scroll to bottom
      if (scrollContainer) {
        scrollContainer.scrollTop = scrollContainer.scrollHeight;
      }
    }
  }

  function scrollToBottom() {
    if (scrollContainer) {
      scrollContainer.scrollTop = scrollContainer.scrollHeight;
    }
  }
</script>

<div class="chat-container">
  <div class="system-prompt-container">
    <details>
      <summary>System Prompt</summary>
      <textarea 
        bind:value={systemPrompt} 
        placeholder="Enter system instructions..."
      ></textarea>
    </details>
  </div>

  <div class="messages-area" bind:this={scrollContainer}>
    {#each messages as message}
      <div class="message-wrapper {message.role}">
        <div class="message-bubble">
          {message.content}
        </div>
      </div>
    {/each}
  </div>

  <div class="input-area">
    <form onsubmit={(e) => { e.preventDefault(); sendMessage(); }}>
      <input 
        type="text" 
        bind:value={input} 
        placeholder="Type a message..." 
        disabled={isStreaming}
      />
      <button type="submit" disabled={isStreaming || !input.trim()}>
        {isStreaming ? '...' : 'Send'}
      </button>
    </form>
  </div>
</div>

<style>
  :global(body) {
    margin: 0;
    font-family: sans-serif;
    background-color: #f4f4f9;
  }

  .chat-container {
    display: flex;
    flex-direction: column;
    height: 100vh;
    max-width: 800px;
    margin: 0 auto;
    border-left: 1px solid #ddd;
    border-right: 1px solid #ddd;
    background-color: white;
  }

  .system-prompt-container {
    padding: 10px;
    background-color: #eee;
    border-bottom: 1px solid #ddd;
  }

  textarea {
    width: 100%;
    height: 60px;
    margin-top: 5px;
    padding: 5px;
    box-sizing: border-box;
    border: 1px solid #ccc;
    border-radius: 4px;
    resize: vertical;
  }

  .messages-area {
    flex: 1;
    overflow-y: auto;
    padding: 20px;
    display: flex;
    flex-direction: column;
    gap: 15px;
  }

  .message-wrapper {
    display: flex;
    width: 100%;
  }

  .message-wrapper.user {
    justify-content: flex-end;
  }

  .message-wrapper.assistant {
    justify-content: flex-start;
  }

  .message-bubble {
    max-width: 70%;
    padding: 10px 15px;
    border-radius: 15px;
    line-height: 1.4;
    word-wrap: break-word;
  }

  .user .message-bubble {
    background-color: #007bff;
    color: white;
    border-bottom-right-radius: 2px;
  }

  .assistant .message-bubble {
    background-color: #e9e9eb;
    color: #333;
    border-bottom-left-radius: 2px;
  }

  .input-area {
    padding: 20px;
    border-top: 1px solid #ddd;
    background-color: white;
  }

  form {
    display: flex;
    gap: 10px;
  }

  input {
    flex: 1;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
    outline: none;
  }

  button {
    padding: 10px 20px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }

  button:disabled {
    background-color: #ccc;
    cursor: not-allowed;
  }
</style>
