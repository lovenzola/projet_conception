from PyQt6.QtCore import QSortFilterProxyModel,Qt

def rechercher_proxy(table_view,champ_recherche, colonne=0):
    modele= table_view.model()
    if not modele:
        return
    
    proxy= QSortFilterProxyModel()
    proxy.setSourceModel(modele)
    proxy.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
    proxy.setFilterKeyColumn(colonne)

    champ_recherche.textChanged.connect(proxy.setFilterFixedString)

    table_view.setModel(proxy)


