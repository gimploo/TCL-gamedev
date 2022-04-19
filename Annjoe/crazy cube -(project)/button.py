import pygame

class Button:
	"""Button class"""
	def __init__(self, x, y, width, height, color, text_size=30, text = '', text_color = (0, 0, 0)):

		self.x = x
		self.y = y 
		self.width = width
		self.height = height
		self.text = text
		self.color = color
		self.text_size = text_size
		self.text_color = text_color
		self.font = pygame.font.SysFont('Impact', self.text_size)

	def draw_button(self, screen):
		pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
		label = self.font.render(self.text, 1, self.text_color)
		screen.blit(label, (self.x + (self.width/2) - (label.get_width()/2), self.y + (self.height/2) - (label.get_height()/2)))

	def check_cursor(self, mousepos):
		"""Checks and returns if mouse cursor is on button or not"""
		m_x = mousepos[0]
		m_y = mousepos[1]

		if self.x <= m_x <= self.x + self.width and self.y <= m_y <= self.y + self.height:
			return True
		else:
			return False 
