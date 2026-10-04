            print(output)
            logger.info(output)
            with open('ucf_analysis.txt', 'a') as f:
                f.write(output)

# Main Test
if __name__ == '__main__':
    start_time = time.time()
    logger.info("Starting UCF Test v5")

    # Load and impute large CSV