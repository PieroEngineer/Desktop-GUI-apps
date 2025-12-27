from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton,
    QGroupBox, QTreeWidget, QTreeWidgetItem, QCheckBox, QDialog
)
from PyQt6.QtCore import Qt

class DataSelectorWindow(QDialog):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Selección de activo")
        self.setMinimumSize(700, 710)

        self.selected_item = None
        
        # Main layout
        self.main_layout = QVBoxLayout()
        
        self.filter_layout = QHBoxLayout()
        self.selection_layout = QHBoxLayout()
        self.decision_layout = QHBoxLayout()

        self.main_layout.addLayout(self.filter_layout)
        self.main_layout.addLayout(self.selection_layout)
        ## Add line here
        self.main_layout.addLayout(self.decision_layout)

        self.init_filter_ui()
        self.init_selection_ui()
        self.init_decision_layout()

        # Complete layout
        self.setLayout(self.main_layout)

    #--UI methods-------------------------------------------------
    def init_filter_ui(self):
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("¿Qué estación buscas?")
        
        # Add this line to connect real-time filtering
        self.search_input.textChanged.connect(self.filter_trees)

        self.filter_layout.addWidget(self.search_input)

    def init_selection_ui(self):

        # Grouping selection areas
        self.pf_group = QGroupBox("Datos del PF")
        self.pf_group_layout = QVBoxLayout(self.pf_group)

        self.pit_group = QGroupBox("Datos del PIT")
        self.pit_group_layout = QVBoxLayout(self.pit_group)

        self.selection_layout.addWidget(self.pf_group)
        self.selection_layout.addWidget(self.pit_group)

        # Adding trees
        self.pf_tree = QTreeWidget()
        self.pf_tree.setHeaderLabels(["Elementos"])
        self.pf_group_layout.addWidget(self.pf_tree)

        self.pit_tree = QTreeWidget()
        self.pit_tree.setHeaderLabels(["Elementos"])
        self.pit_group_layout.addWidget(self.pit_tree)
    
    def init_decision_layout(self):
        self.accept_btn = QPushButton("Aceptar")
        self.online_switch = QCheckBox("Datos online")

        self.decision_layout.addWidget(self.accept_btn)
        self.decision_layout.addWidget(self.online_switch)

    #--Building methods-------------------------------------------------
    def populate_tree(self, data_dict: dict, tree:str):
        for parent, children in data_dict.items():
            parent_item = QTreeWidgetItem([parent])
            parent_item.setFlags(parent_item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            if tree == 'pf':
                self.pf_tree.addTopLevelItem(parent_item)
            else:
                self.pit_tree.addTopLevelItem(parent_item)

            for child in children:
                child_item = QTreeWidgetItem([child])
                child_item.setFlags(child_item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
                child_item.setCheckState(0, Qt.CheckState.Unchecked)
                parent_item.addChild(child_item)

    def uncheck_all(self):
        """Unchecks all checkable items in a QTreeWidget, skipping top-level items."""
        
        def uncheck_all_children(item: QTreeWidgetItem):
            """Recursively unchecks all checkable children of a given QTreeWidgetItem."""
            for i in range(item.childCount()):
                child = item.child(i)
                if child.flags() & Qt.ItemFlag.ItemIsUserCheckable:
                    child.setCheckState(0, Qt.CheckState.Unchecked)
                uncheck_all_children(child) # Recurse for grand-children
        
        for i in range(self.pf_tree.topLevelItemCount()):
            top_level_item = self.pf_tree.topLevelItem(i)
            uncheck_all_children(top_level_item)

        for i in range(self.pit_tree.topLevelItemCount()):
            top_level_item = self.pit_tree.topLevelItem(i)
            uncheck_all_children(top_level_item)

    def filter_trees(self, text):
        """Filters both trees based on the search text, keeping parents visible if they or their children match."""
        search_text = text.lower()

        def filter_item(item: QTreeWidgetItem):
            # Check if the item itself matches
            item_matches = search_text in item.text(0).lower()
            
            # Check if any child matches (recurse first)
            has_matching_child = False
            for i in range(item.childCount()):
                child = item.child(i)
                child_visible = filter_item(child)  # Recursive call
                if child_visible:
                    has_matching_child = True
            
            # Decide if item should show
            show_item = item_matches or has_matching_child
            item.setHidden(not show_item)
            
            # If showing the item (parent), expand it and force ALL children visible (override their hidden state)
            if show_item and item.childCount() > 0:
                item.setExpanded(True)
                for i in range(item.childCount()):
                    item.child(i).setHidden(False)
            
            return show_item

        # Apply to both trees
        for tree in [self.pf_tree, self.pit_tree]:
            for i in range(tree.topLevelItemCount()):
                top_item = tree.topLevelItem(i)
                filter_item(top_item)
            
            # If search is empty, show all but collapse for clean view
            if not search_text:
                tree.collapseAll()