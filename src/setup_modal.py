from nextcord import ui, TextInputStyle, Interaction


class SetupModal(ui.Modal):
    def __init__(self):
        super().__init__(
            title="Setup",
            timeout=None,
            custom_id="persistent_modal:Setup",
        )
        self.setup = ui.TextInput(
            label="Enter your config below",
            placeholder="Firebase config",
            style=TextInputStyle.paragraph,
            required=True,
            custom_id="persistent_modal:setup_box",
        )
        self.add_item(self.setup)

    async def callback(self, interaction: Interaction):
        with open("config.py", "w") as f:
            f.write(f"firebaseConfig = {{{self.setup.value}}}")
        await interaction.send(
            f"Config setup"
        )
