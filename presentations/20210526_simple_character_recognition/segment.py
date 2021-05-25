from image import image

# segment the truth data
truth = image('truth.bin')
truth.segment([745, 838, 932])

# segment the test data
test = image('test.bin')
test.segment()
