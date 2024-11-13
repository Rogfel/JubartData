import datetime
from typing import Optional, Union
from dateutil import parser
import re

class DateParser:
    def __init__(self, default_year: Optional[int] = None):
        self.default_year = default_year or datetime.datetime.now().year
        
        # Padrões regex para diferentes formatos de data
        self.patterns = {
            'dd/mm/yyyy': r'^(\d{2})/(\d{2})/(\d{4})$',
            'dd/mm': r'^(\d{2})/(\d{2})$',
            'yyyy_mm_dd': r'^(\d{4})_(\d{2})_(\d{2})$',
            'yyyy-mm-dd': r'^(\d{4})-(\d{2})-(\d{2})$'
        }
        
    def parse(self, date_string: str) -> Optional[datetime.datetime]:
        """
        Analisa uma string de data em vários formatos e retorna um objeto datetime.
        
        Args:
            date_string: String contendo a data
            
        Returns:
            datetime object ou None se a data for inválida
        """
        if not date_string or not isinstance(date_string, str):
            return None
            
        # Limpar a string
        date_string = date_string.strip()
        
        # Tentar cada padrão
        for format_name, pattern in self.patterns.items():
            match = re.match(pattern, date_string)
            if match:
                try:
                    if format_name == 'dd/mm/yyyy':
                        day, month, year = map(int, match.groups())
                        return datetime.datetime(year, month, day)
                        
                    elif format_name == 'dd/mm':
                        day, month = map(int, match.groups())
                        return datetime.datetime(self.default_year, month, day)
                        
                    elif format_name in ['yyyy_mm_dd', 'yyyy-mm-dd']:
                        year, month, day = map(int, match.groups())
                        return datetime.datetime(year, month, day)
                        
                except ValueError:
                    continue
        
        # Tentar parse com dateutil como fallback
        try:
            return parser.parse(date_string)
        except (ValueError, TypeError):
            return None
                
    def format_date(self, date_string: str, output_format: str = '%Y-%m-%d') -> Optional[str]:
        """
        Analisa e formata uma string de data para o formato especificado.
        
        Args:
            date_string: String contendo a data
            output_format: Formato de saída desejado
            
        Returns:
            String formatada ou None se a data for inválida
        """
        parsed_date = self.parse(date_string)
        if parsed_date:
            return parsed_date.strftime(output_format)
        return None

# Exemplo de uso
def main():
    # Criar instância do parser
    parser = DateParser(default_year=2024)
    
    # Lista de datas para testar
    test_dates = [
        '25/12/2023',  # dd/mm/yyyy
        '15/03',       # dd/mm
        '2023_12_25',  # yyyy_mm_dd
        '2023-12-25',  # yyyy-mm-dd
        'invalid',     # data inválida
        '29/02/2024',  # data válida (ano bissexto)
        '29/02/2023'   # data inválida (não é ano bissexto)
    ]
    
    print("Testando parser de datas:")
    print("-" * 50)
    
    for date_str in test_dates:
        parsed_date = parser.parse(date_str)
        formatted_date = parser.format_date(date_str)
        
        print(f"\nData original: {date_str}")
        print(f"Parsed: {parsed_date}")
        print(f"Formatada: {formatted_date}")

if __name__ == "__main__":
    main()
