def convert_to_lower(input):
    """ Return list of input items in lower case """
    if not input:
        return []
    else:
        last_item = input[-1]
        rest_of_list = input[:-1]
        return convert_to_lower(rest_of_list) + [last_item.lower()]
    # return [] if not input else convert_to_lower(input[:-1]) + [input[-1].lower()]


names = ['Anne', 'BILL', 'CiCi', 'dee']
print(f'original list: {names}')
lower_names = convert_to_lower(names)
print(f'list after recursive processing: {lower_names}')


def list_sum(nums):
    """ Recursive list summation """
    if not nums:
        return 0
    else:
        first_item = nums[0]
        rest_of_list = nums[1:]
        return first_item + list_sum(rest_of_list)
    # return 0 if not nums else nums[0] + list_sum(nums[1:])


values = [10, 20, 30, 40]

sum = list_sum(values)

print(f'sum of values {values} is {sum}')