#                   DEFINITION DU STYLE DES ONGLETS ET PAGES
#--------------------------------------------------------------------------------------------------------------

THEME = """
QWidget {
    background-color:white;  
    color: black;
    font-family: 'Segoe UI', sans-serif;
    font-size: 14px;
}

QTableView {
    background-color: white; /* Fond général */
    alternate-background-color: #F2F7FC; /* Bleu très pâle */
    color: black;
    border: none;
    gridline-color: #DCE3ED;
    selection-background-color: #D9E6F2; /* Bleu clair pour la sélection */
    selection-color: #1A1C2C;
    font-size: 13px;
}

QHeaderView::section {
    background-color: rgba(0,120,215, 0.75); /* Entête colorée */
    color: white;
    font-weight: bold;
    padding: 6px;
    border: 1px solid white;
}

QTabBar::tab {
    background-color:  rgba(0,120,215, 0.75);
    color: white;
    padding: 8px 20px;
    font-weight: bold;
    border: 1px solid white;
    border-bottom: none;
}
QTabBar::tab:selected {
    background-color: #F2F7FC;
    color: black;
    border: 0.5px solid rgba(0,120,215, 0.75);
}

QToolBox::tab {
    background-color:rgba(255,0,0,0.9) ;
    border: none;
    border-radius: 3px;
    font-style: italic;
    font-weight: bold;
    color: white;
}
QToolBox::tab::selected{
    background-color: rgba(255,0,0,0.5);
    border: 0.5px solid rgba(255,0,0,0.9) ;
    color: white;
    font-weight: bold;
}

QPushButton {
    background-color: rgba(0,120,215, 0.75);
    color: white;
    font-weight: bold;
    border: none;
    border: 1px solid white;
    padding: 6px 12px;
    border-radius: 10px;
}
QPushButton::pressed{
    background-color: #F2F7FC;
    color: black;
    border: 0.5px solid rgba(0,120,215, 0.75);
}
QPushButton:checked{
    background-color: #F2F7FC;
    color: black;
    border: 0.5px solid rgba(0,120,215, 0.75);
}


QLineEdit, QComboBox{
    color: black;
    border: 1px solid #4A5060;
    border-radius: 3px;
    padding: 4px;
}

QScrollBar:vertical {
    background-color:  rgba(0,120,215, 0.75);
    width: 12px;
    margin: 2px;
}
QScrollBar::handle:vertical {
    background-color: rgba(0,120,215, 0.75);
    min-height: 20px;
    border-radius: 4px;
}
QScrollBar:horizontal {
    background-color:  rgba(0,120,215, 0.75);
    min-width: 10px;
    margin: 2px;
}
QScrollBar::handle:horizontal {
    background-color: rgba(0,120,215, 0.75);
    height: 8px;
    border-radius: 4px;
}

#group_principal{
    subcontrol-position: top left;
    font-size: 18px;
    font-weight:bold;
}
#sous_group{
    subcontrol-position: top center;
    font-weight:bold;
    font-style: italic;
}

#onglet_stats{
    font-size: 20px;
    font-weight:bold;
    font-style: italic;
}


"""











