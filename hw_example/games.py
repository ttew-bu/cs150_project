#### You may assume that in mixed-objectives games, the first action is the cooperative one (remain silent, play dove, etc.)

PD = [('Cooperate', 'Defect'), {
        ('Cooperate', 'Cooperate'): (-1, -1),
        ('Cooperate', 'Defect'): (-5, 0),
        ('Defect', 'Cooperate'): (0, -5),
        ('Defect', 'Defect'): (-3, -3)
    }]

Chicken = [('Dove', 'Hawk'), {
        ('Dove', 'Dove'): (0, 0),
        ('Dove', 'Hawk'): (-1, 5),
        ('Hawk', 'Dove'): (5, -1),
        ('Hawk', 'Hawk'): (-10, -10)
    }]

ThreeChoices = [('A', 'B', 'C'), {
    ('A', 'A'): (2,2),    ('A', 'B'): (0,3),    ('A', 'C'): (3,0),
    ('B', 'A'): (0,3),    ('B', 'B'): (2,2),    ('B', 'C'): (3,0),
    ('C', 'A'): (3,0),    ('C', 'B'): (0,3),    ('C', 'C'): (2,2)
    }]