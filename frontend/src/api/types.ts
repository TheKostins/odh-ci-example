interface Topic {
	id: number;
	name: string;
}
interface Message {
	author_nickname: string;
	content: string;
	time_created: string;
}

interface MessagesResponse {
	limit: number;
	offset: number;
	total: number;
	items: Message[];
}

interface TopicsResponse {
	total: number;
	offset: number;
	limit: number;
	items: Topic[];
}
export type { Topic, TopicsResponse, Message, MessagesResponse };
