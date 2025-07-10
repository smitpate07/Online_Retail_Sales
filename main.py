from online_retail.data_transformation import DataTransformation
from online_retail.report_generator import ReportGenerator
from online_retail.image_generator import ImageGenerator

def main():
    while True:
        try:
            user_input = int(input("Please select a report level (1 = Basic, 2 = Standard, 3 = Full). Press Enter: "))
            if user_input in [1, 2, 3]:
                break
            else:
                print("Invalid input. Please enter 1, 2, or 3.")
        except ValueError:
            print("Invalid input. Please enter a number (1, 2, or 3).")

    data_transformation = DataTransformation()
    data_transformation.data_transformation()
    data_transformation.clean_data()
    image_generator = ImageGenerator(data_transformation)
    report_generator = ReportGenerator(data_transformation, image_generator=image_generator)
    report_generator.report_generator(mode=user_input)
  
if __name__=="__main__":
    main()