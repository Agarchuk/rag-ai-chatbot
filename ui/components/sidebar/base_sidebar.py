class BaseSidebar:
    def __init__(self):
        self.components = []
        
    def add_component(self, component):
        self.components.append(component)
        
    def display(self):
        for component in self.components:
            component.display()