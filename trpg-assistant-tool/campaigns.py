from storage import load_campaigns, save_campaigns


def create_campaign(data):
    campaigns = load_campaigns()
    campaigns.append(data)
    save_campaigns(campaigns)


def get_all_campaigns():
    return load_campaigns()


def update_campaign(index, data):
    campaigns = load_campaigns()

    if index < 0 or index >= len(campaigns):
        return False

    campaigns[index] = data
    save_campaigns(campaigns)
    return True


def delete_campaign(index):
    campaigns = load_campaigns()

    if index < 0 or index >= len(campaigns):
        return False

    campaigns.pop(index)
    save_campaigns(campaigns)
    return True
