import pygame, random

class Abilities:
	"""abilities"""
	def __init__(self):
		self.abilities = {'health': 0, 'time freeze': 0, 'gravity aura': 0, 'shield': 0, 'score bag': 0}
		self.rarity = {'health': 3, 'time freeze': 12, 'gravity aura': 12,  'score bag': 15, 'shield': 7}
		#self.rarity = {'health': 1, 'time freeze': 1, 'gravity aura': 1, 'shield': 1, 'score bag': 1} #for testing

	def ability_generator(self):
		power_ups = []
		for power_up in self.abilities:
			power_ups.append(power_up)

		power_up_choice = random.choice(power_ups)
		self.abilities[power_up_choice] += 1
		while self.abilities[power_up_choice] != self.rarity[power_up_choice]:
			power_up_choice = random.choice(power_ups)
			self.abilities[power_up_choice] += 1

		ability = power_up_choice
		#print(self.abilities)
		for _ in self.abilities:
			if _ == ability:
				self.abilities[_] = 0
			elif _ != ability and self.abilities[_] > 0:
				self.abilities[_] -= random.randint(1, 4)
				if self.abilities[_] < 0:
					self.abilities[_] = 0
		
		if ability == 'score bag':
			radius = random.randint(10, 40)
		else:
			radius = 10

		return ability, radius

	def ability_render(self, new_ability, surface, center_list, radius):
		"""REnders ability powerup"""
		
		width = 0

		if new_ability == 'health':
			color = (255, 0, 0)


		elif new_ability == 'time freeze':
			color = (0, 255, 0)

		elif new_ability == 'gravity aura':
			color = (0, 255, 255)

		elif new_ability == 'shield':
			color = (200, 253, 15)

		elif new_ability == 'score bag':
			color = (215, 105, 156)
			

		pygame.draw.circle(surface, color, center_list, radius, width)



			

	def ability_effect_render(self, active_ability, passed_time, ability_dict, stored_abilities, enemy_rect, player_feat, enemy_list, enemy, enemy_index, surface):
		"""ability effect"""
		effective_time = {'time freeze' : 10, 'shield' : 15, 'gravity aura': 20}

		if passed_time < effective_time[active_ability]:

			if active_ability == 'time freeze':
				vel_x = 0
				vel_y = 0
				#if enemy_rect.colliderect(player_rect):
				#	enemy_list.pop(enemy_index)

			elif active_ability == 'shield':
				radius = 1.7 * player_feat[0].get_width()
				player_rect = player_feat[1]
				pygame.draw.circle(surface, (255, 255, 0), player_rect.center, radius)

			elif active_ability == 'gravity aura':
				radius = 1.6 * player_feat[0].get_width()
				player_rect = player_feat[1]
				pygame.draw.circle(surface, (51, 255, 153), player_rect.center, radius)




		else:

			del ability_dict[active_ability]
			#stored_abilities[active_ability] -= 1
			#if stored_abilities[active_ability] == 0:
			#	del stored_abilities[active_ability]
			enemy[7] = False

			
	
	
