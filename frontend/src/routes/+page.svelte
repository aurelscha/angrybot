<script>
	import autoAnimate from '@formkit/auto-animate';
	let responseData = $state('');
	let userMessage = $state('');
	let chatHistory = $state([]);
	let messages;

	async function chat() {
		chatHistory.push({ author: 'user', message: userMessage });
		let message = userMessage;
		userMessage = '';
		const response = await fetch('http://localhost:8000/chat', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ message: message })
		});

		// Create a readable stream from the response body
		const reader = response.body.getReader();
		const decoder = new TextDecoder();
		let done = false;
		let result = '';

		// Read the stream as it comes in
		while (!done) {
			messages.scrollTo({
				top: messages.scrollHeight,
				behavior: 'smooth'
			});
			const { value, done: readerDone } = await reader.read();
			done = readerDone;

			// Decode the chunk and append to the result
			result += decoder.decode(value, { stream: true });

			// You can update your UI with the streamed content
			responseData = result;
		}
		chatHistory.push({ author: 'ai', message: responseData });
		responseData = '';
	}
</script>

{#snippet avatar(author)}
	{#if author == 'ai'}
		<div class="author">
			<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24"
				><!-- Icon from All by undefined - undefined --><path
					fill="currentColor"
					d="M22 14h-1c0-3.87-3.13-7-7-7h-1V5.73A2 2 0 1 0 10 4c0 .74.4 1.39 1 1.73V7h-1c-3.87 0-7 3.13-7 7H2c-.55 0-1 .45-1 1v3c0 .55.45 1 1 1h1v1a2 2 0 0 0 2 2h14c1.11 0 2-.89 2-2v-1h1c.55 0 1-.45 1-1v-3c0-.55-.45-1-1-1M7.5 18A2.5 2.5 0 0 1 5 15.5c0-.82.4-1.54 1-2l3.83 2.88C9.5 17.32 8.57 18 7.5 18m9 0c-1.07 0-2-.68-2.33-1.62L18 13.5c.6.46 1 1.18 1 2a2.5 2.5 0 0 1-2.5 2.5"
				/></svg
			>
		</div>
	{/if}
{/snippet}

<main class="ai">
	<div class="logo">
		<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24"
			><!-- Icon from All by undefined - undefined --><path
				fill="white"
				d="M22 14h-1c0-3.87-3.13-7-7-7h-1V5.73A2 2 0 1 0 10 4c0 .74.4 1.39 1 1.73V7h-1c-3.87 0-7 3.13-7 7H2c-.55 0-1 .45-1 1v3c0 .55.45 1 1 1h1v1a2 2 0 0 0 2 2h14c1.11 0 2-.89 2-2v-1h1c.55 0 1-.45 1-1v-3c0-.55-.45-1-1-1M7.5 18A2.5 2.5 0 0 1 5 15.5c0-.82.4-1.54 1-2l3.83 2.88C9.5 17.32 8.57 18 7.5 18m9 0c-1.07 0-2-.68-2.33-1.62L18 13.5c.6.46 1 1.18 1 2a2.5 2.5 0 0 1-2.5 2.5"
			/></svg
		>
	</div>
	<div class="chat">
		<div class="messages" bind:this={messages}>
			{#each chatHistory as { author, message }}
				<div class={['message', `message--${author}`]}>
					{@render avatar(author)}
					<div class="message__content">
						{message}
					</div>
				</div>
			{/each}
			{#if responseData}
				<div class="message message--ai">
					{@render avatar('ai')}
					<div class="message__content">{responseData}</div>
				</div>
			{/if}
		</div>
		<div class="bar">
			<input
				bind:value={userMessage}
				placeholder="Let's go"
				onkeypress={(e) => e.key === 'Enter' && chat()}
			/>
			<button onclick={chat}
				><svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24"
					><!-- Icon from All by undefined - undefined --><path
						fill="currentColor"
						fill-rule="evenodd"
						d="M3.291 3.309a.75.75 0 0 0-.976.996l3.093 6.945H13a.75.75 0 0 1 0 1.5H5.408l-3.093 6.945a.75.75 0 0 0 .976.996l19-8a.75.75 0 0 0 0-1.382z"
						clip-rule="evenodd"
					/></svg
				></button
			>
		</div>
	</div>
</main>

<style lang="scss">
	.ai {
		height: 100vh;
		width: 100vw;
		padding: 24px;
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 24px;
		min-height: 0;
	}
	.logo {
		flex-shrink: 0;
	}
	.chat {
		display: flex;
		flex-direction: column;
		gap: 1rem;
		width: 100%;
		height: 100%;
		flex: 1;
		margin: 0 auto;
		max-width: 1024px;
		min-height: 0;
	}
	.messages {
		display: flex;
		flex-direction: column;
		height: 100%;
		background: red;
		overflow-y: auto;
		background: #111827;
		border-radius: 4px;
		padding: 24px;
		gap: 6px;
	}
	.message {
		color: white;
		display: flex;
		gap: 12px;
		width: 100%;
		justify-content: flex-start;
		flex-direction: row-reverse;
		white-space: pre-line;
		.message__content {
			border-radius: 12px 0 12px 12px;
		}
	}
	.message--ai {
		flex-direction: row;
		width: 100%;

		.message__content {
			border-radius: 0 12px 12px 12px;
			background: #1f2937;
			border: none;
		}
	}
	.message__content {
		border: 1px solid #374151;
		padding: 12px 16px;
	}
	.bar {
		display: flex;
		height: fit-content;
		background: #111827;
		border-radius: 4px;
		padding: 24px;
		gap: 12px;
	}
	input {
		background: none;
		border: 2px solid #374151;
		outline: none;
		padding: 12px;
		width: 100%;
		border-radius: 4px;
		height: 60px;
		color: white;
		font-size: 16px;
		&::placeholder {
			color: #374151;
		}
	}
	button {
		outline: none;
		border: none;
		background: #0ea5e9;
		color: white;
		border-radius: 4px;
		padding-inline: 12px;
		transition: all 0.2s ease;
		&:hover {
			background: #0c87c8;
			cursor: pointer;
		}
	}
</style>
