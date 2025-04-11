<script lang="ts">
	import { onMount } from 'svelte';
	import type { MessagesResponse, Topic } from '../../../api/types';
	import MessageComponent from '../../../components/MessageComponent.svelte';
	import { page } from '$app/state';
	const topicId = page.params.id;

	let messages = $state({} as MessagesResponse);
	let topic = $state({} as Topic);

	onMount(async () => {
		const topicResponse = await fetch(`/api/v1/topics/${topicId}`);
		topic = await topicResponse.json();

		const messagesResponse = await fetch(`/api/v1/topics/${topicId}/messages`);
		messages = await messagesResponse.json();
	});

	let messageContents = $state('');
	let nickname = $state('');
	const handleCreateMessage = () => {
		if (nickname && messageContents) {
			fetch(`/api/v1/topics/${topic.id}/messages`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					author_nickname: nickname,
					content: messageContents
				})
			})
				.then(() => fetch(`/api/v1/topics/${topic.id}/messages`))
				.then((response) => response.json())
				.then((data) => data as MessagesResponse)
				.then((data) => {
					messages = data;
					messageContents = '';
				});
		}
	};
</script>

<div class="flex space-x-2 pl-20 pt-10 text-xl flex-col space-y-5">
	<div>
		<p class="inline">Добро пожаловать в</p>
		<p class="font-bold inline">{topic.name}</p>
		<a href="/">На главную</a>
	</div>
	<div class="w-100 space-y-2">
		<div class="flex w-full space-x-2">
			<input
				type="text"
				class="bg-stone-300 text-center text-stone-600 w-68"
				placeholder="Введите ник"
				bind:value={nickname}
			/>
			<button class="h-8 bg-stone-300 text-stone-600 w-30" onclick={() => handleCreateMessage()}
				>Отправить</button
			>
		</div>
		<textarea
			class="bg-stone-300 text-stone-600 h-16 w-100 resize-y"
			placeholder="Текст сообщения"
			bind:value={messageContents}
		></textarea>
	</div>

	<div class="flex flex-col space-y-2 w-100">
		{#each messages.items as message, i (i)}
			<MessageComponent {message} />
		{/each}
	</div>
</div>
