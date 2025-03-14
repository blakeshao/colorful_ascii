export interface ASCIIConfig {
    font_size: number;
    font_path: string;
    background_color: [number, number, number];
    characters: ASCIICharacter[];
    original_color: boolean;
}

export interface ASCIICharacter {
    char: string;
    threshold: [number, number];
    color: [number, number, number];
}