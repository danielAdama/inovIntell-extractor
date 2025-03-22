import argparse
from extractor.rwe_extractor import RWEExtractor

file_path = '/Users/danny/Desktop/programming/NLP/inovIntell-extractor/Banna 2022.pdf'

def main():
    parser = argparse.ArgumentParser(description='Extract RWE data from PDF')
    parser.add_argument('pdf_path', help='Path to the PDF file')
    parser.add_argument('--wandb-project', default='rwe-extraction-demo',
                      help='W&B project name')
    
    args = parser.parse_args()
    
    extractor = RWEExtractor(wandb_project=args.wandb_project)
    extractor.process_and_log(args.pdf_path)

if __name__ == "__main__":
    main()