class TorneoSuperior:
    def __init__(self, campeones):
        self.campeones = campeones

    def __repr__(self):
        return f"<TorneoSuperior con {len(self.campeones)} campeones>"
