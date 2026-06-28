import api_request
import response_parser


def main():
    raw_data = api_request.make_request()
    simplified_data = response_parser.raw_to_price_gap(raw_data)
    response_parser.print_sorted_output(simplified_data)


if __name__ == "__main__":
    main()
