cmake_minimum_required(VERSION 3.15.3)

project(BMS-Interface)

enable_language(C CXX ASM)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_C_STANDARD 99)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_C_EXTENSIONS OFF)


set(STM32CUBEMX_GENERATED_FILES

        Core/Src/stm32g0xx_it.c
        Core/Src/stm32g0xx_hal_msp.c
        Drivers/STM32G0xx_HAL_Driver/Src/stm32g0xx_hal_spi.c
        Drivers/STM32G0xx_HAL_Driver/Src/stm32g0xx_hal_spi_ex.c
        Drivers/STM32G0xx_HAL_Driver/Src/stm32g0xx_hal_rcc.c
        Drivers/STM32G0xx_HAL_Driver/Src/stm32g0xx_hal_rcc_ex.c
        Drivers/STM32G0xx_HAL_Driver/Src/stm32g0xx_ll_rcc.c
        Drivers/STM32G0xx_HAL_Driver/Src/stm32g0xx_hal_flash.c
        Drivers/STM32G0xx_HAL_Driver/Src/stm32g0xx_hal_flash_ex.c
        Drivers/STM32G0xx_HAL_Driver/Src/stm32g0xx_hal_gpio.c
        Drivers/STM32G0xx_HAL_Driver/Src/stm32g0xx_hal_dma.c
        Drivers/STM32G0xx_HAL_Driver/Src/stm32g0xx_hal_dma_ex.c
        Drivers/STM32G0xx_HAL_Driver/Src/stm32g0xx_ll_dma.c
        Drivers/STM32G0xx_HAL_Driver/Src/stm32g0xx_hal_pwr.c
        Drivers/STM32G0xx_HAL_Driver/Src/stm32g0xx_hal_pwr_ex.c
        Drivers/STM32G0xx_HAL_Driver/Src/stm32g0xx_hal_cortex.c
        Drivers/STM32G0xx_HAL_Driver/Src/stm32g0xx_hal.c
        Drivers/STM32G0xx_HAL_Driver/Src/stm32g0xx_hal_exti.c
        Drivers/STM32G0xx_HAL_Driver/Src/stm32g0xx_hal_tim.c
        Drivers/STM32G0xx_HAL_Driver/Src/stm32g0xx_hal_tim_ex.c
        Drivers/STM32G0xx_HAL_Driver/Src/stm32g0xx_hal_uart.c
        Drivers/STM32G0xx_HAL_Driver/Src/stm32g0xx_hal_uart_ex.c
        Core/Src/system_stm32g0xx.c 

        Core/Inc/main.h
        Core/Inc/stm32g0xx_hal_conf.h
        Core/Inc/stm32g0xx_it.h

        Core/Src/main.cpp

        startup_stm32g0b1xx.s)

set(EXECUTABLE ${PROJECT_NAME}.elf)

add_executable(${EXECUTABLE} ${STM32CUBEMX_GENERATED_FILES})

target_compile_definitions(${EXECUTABLE} PRIVATE
        -DUSE_HAL_DRIVER
        -DSTM32G0B1xx
        )

target_include_directories(${EXECUTABLE} PRIVATE
        Core/Inc
        Drivers/STM32G0xx_HAL_Driver/Inc
        Drivers/CMSIS/Device/ST/STM32G0xx/Include
        Drivers/CMSIS/Include
        modules/MAX17843
        modules/MAX17851
        )

target_compile_options(${EXECUTABLE} PRIVATE
        -mcpu=cortex-m0plus
        -mthumb
        -mfpu=fpv4-sp-d16

        -fdata-sections
        -ffunction-sections

        -Wall
        $<$<CONFIG:Debug>:-0g>
        )

target_link_options(${EXECUTABLE} PRIVATE
        -T${CMAKE_SOURCE_DIR}/STM32G0B1KETxN_FLASH.ld
        -mcpu=cortex-m0plus
        -mthumb
        -mfpu=fpv4-sp-d16
        -mfloat-abi=hard
        -specs=nano.specs
        -lc
        -lm
        -lnosys
        -Wl,-Map=${PROJECT_NAME}.map,--cref
        -Wl,--gc-sections
        )

# Print executable size
add_custom_command(TARGET ${EXECUTABLE}
        POST_BUILD
        COMMAND arm-none-eabi-size ${EXECUTABLE})

# Create hex file
add_custom_command(TARGET ${EXECUTABLE}
        POST_BUILD
        COMMAND arm-none-eabi-objcopy -O ihex ${EXECUTABLE} ${PROJECT_NAME}.hex
        COMMAND arm-none-eabi-objcopy -O binary ${EXECUTABLE} ${PROJECT_NAME}.bin)