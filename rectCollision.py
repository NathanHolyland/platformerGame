import pygame


def handleCollision(rect1, rect2):
    # with respect to rect 1
    result1 = False
    xCondition1 = (rect2[0] <= rect1[0]+rect1[2] <= rect2[0]+rect2[2])
    xCondition2 = (rect2[0] <= rect1[0] <= rect2[0]+rect2[2])
    yCondition1 = (rect2[1] <= rect1[1]+rect1[3] <= rect2[1]+rect2[3])
    yCondition2 = (rect2[1] <= rect1[1] <= rect2[1]+rect2[3])
    if xCondition1 or xCondition2:
        if yCondition1 or yCondition2:
            result1 = True

    # with respect to rect 2
    result2 = False
    xCondition1 = (rect1[0] <= rect2[0]+rect2[2] <= rect1[0]+rect1[2])
    xCondition2 = (rect1[0] <= rect2[0] <= rect1[0]+rect1[2])
    yCondition1 = (rect1[1] <= rect2[1]+rect2[3] <= rect1[1]+rect1[3])
    yCondition2 = (rect1[1] <= rect2[1] <= rect1[1]+rect1[3])

    # Vector from rect1 to rect2
    center1 = [rect1[0]+rect1[2]/2, rect1[1]+rect1[3]/2]
    center2 = [rect2[0] + rect2[2] / 2, rect2[1] + rect2[3] / 2]
    vector = [center2[0]-center1[0], center2[1]-center1[1]]

    if xCondition1 or xCondition2:
        if yCondition1 or yCondition2:
            result2 = True

    if abs(vector[0]) >= abs(vector[1]):
        if vector[0] < 0:
            correction = [(rect2[0]+rect2[2])-rect1[0], 0]
        else:
            correction = [rect2[0]-(rect1[0]+rect1[2]), 0]
    else:
        if vector[1] < 0:
            correction = [0, (rect2[1] + rect2[3]) - rect1[1]]
        else:
            correction = [0, rect2[1]-(rect1[1]+rect1[3])]

    if result1 or result2:
        return True, correction
    return False, [0, 0]


def testEnvironment():
    screen = pygame.display.set_mode([500, 500])
    r1 = [175, 175, 100, 100]
    r2 = [200, 165, 50, 10]

    running = True
    while running:
        screen.fill((255, 255, 255))
        pygame.draw.rect(screen, (255, 0, 0), r1, 0)
        pygame.draw.rect(screen, (0, 0, 255), r2, 0)
        pygame.display.flip()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            r2[1] += -0.25
        if keys[pygame.K_s]:
            r2[1] += 0.25
        if keys[pygame.K_d]:
            r2[0] += 0.25
        if keys[pygame.K_a]:
            r2[0] += -0.25
        if keys[pygame.K_UP]:
            r2[2] += 0.25
            r2[3] += 0.25
        if keys[pygame.K_DOWN]:
            r2[2] += -0.25
            r2[3] += -0.25

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    collision, correction = handleCollision(r1, r2)
                    print(collision)
                    print(correction)
                    if collision:
                        r1[0] += correction[0]
                        r1[1] += correction[1]
    pygame.quit()



