class Dialogue:
	def __init__(self, content):
		self.content = content
		self.next_dialogue = None

	def get_content(self):
		return self.content

test_dialogue = Dialogue(
	"I hope the day has found you well, sir. I need a longer line of dialogue."
	)
linked_dialogue = Dialogue("Farewell, good sir.")
test_dialogue.next_dialogue = linked_dialogue

innkeeper_dialogue = Dialogue("I am just an innkeeper, Mr. Adventurer.")

dog_dialogue = Dialogue("Woof! Woof!!")