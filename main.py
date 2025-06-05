from organizer import ConferenceOrganizer


def main():
    """Função principal que executa a organização das palestras"""
    organizer = ConferenceOrganizer()
    
    # Ler e parsear palestras do arquivo
    talks = organizer.parse_talks("proposals.txt")
    
    # Organizar em tracks
    tracks = organizer.organize_tracks(talks)
    
    # Formatar e exibir resultado
    output = organizer.format_output(tracks)
    print(output)


if __name__ == "__main__":
    main()